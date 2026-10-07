#!/usr/bin/env python3
"""
Extrae los precios del Suzuki Fronx desde Chileautos y Yapo, y actualiza
precios/data/ultimo.json con las categorias: manual, automatica, maximo,
nuevo, nuevo_bono.

Por que Playwright y no urllib/requests:
- Chileautos renderiza los precios en el HTML inicial (SSR), pero Yapo es
  una SPA que carga los precios despues via JavaScript. Un fetch simple
  (urllib) nunca ve esos precios en Yapo. Playwright abre un navegador
  real, espera a que cargue, y lee el contenido ya renderizado -- funciona
  igual para ambos sitios.

Como se extraen precio y transmision (importante para mantenimiento):
- Se ejecuta JavaScript dentro de la pagina (page.evaluate) que busca
  elementos cuyo texto propio (sin hijos) matchee "$ X.XXX.XXX", y sube
  por los ancestros hasta encontrar el link <a> del aviso (para no
  contar el mismo aviso dos veces -- cada aviso muestra el precio en
  mas de un lugar en el DOM). Luego revisa el texto de ese aviso
  completo buscando la palabra "Manual" o "Automatica".
- Este enfoque (JS ejecutado en el navegador, no un selector CSS fijo de
  Playwright con .nth()) se valido manualmente contra las paginas reales
  de Chileautos y Yapo el 2026-10-07 antes de escribir este script:
  extrajo correctamente los 8 avisos de Chileautos y los 5 de Yapo,
  verificados uno por uno contra lo que se ve en pantalla.

Controles de calidad de dato (agregados 2026-10-07, tras revision externa):
- palabra_obligatoria (de modelos.json) filtra avisos que no mencionan el
  modelo exacto, para no mezclar otro auto que haya aparecido en la busqueda.
- Se exige un minimo de avisos POR FUENTE (no solo el total combinado), asi
  una sola fuente nunca puede definir el precio por si sola.
- Deduplicacion cross-source conservadora (precio+anio+transmision) para no
  contar dos veces el mismo auto publicado en ambos portales.
- Si el precio calculado se aleja mas de VARIACION_MAX_PORCENTAJE del valor
  del dia anterior, se trata como sospechoso y se reintenta en vez de
  publicarlo.
Quedan fuera de esta ronda (pendientes para una segunda etapa, a pedido
explicito de Cata): la formula nuevo/nuevo_bono, deteccion de outliers
estadisticos, y el historial de precios mas alla de ultimo.json.
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE, "config", "modelos.json")
DATA = os.path.join(BASE, "data")
ULTIMO = os.path.join(DATA, "ultimo.json")

ALERTA_EMAIL = "catalinamarin@skalling.com"
UNIDAD_BASE_URL = "https://www.unidadcreditos.cl"


def enviar_alerta(asunto, cuerpo):
    """Manda un correo via Outlook (usa la cuenta ya logueada en este
    computador, sin necesitar ninguna contraseña nueva). Si Outlook no
    esta instalado o falla, solo lo imprime en pantalla -- nunca detiene
    el script por esto."""
    try:
        import win32com.client  # type: ignore

        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = ALERTA_EMAIL
        mail.Subject = asunto
        mail.Body = cuerpo
        mail.Send()
        print(f"  Alerta enviada por correo a {ALERTA_EMAIL}")
    except Exception as e:
        print(f"  No se pudo enviar la alerta por correo ({e}). Aviso solo queda en este log:")
        print(f"  ASUNTO: {asunto}")
        print(f"  CUERPO: {cuerpo}")

HOY = datetime.now(timezone(timedelta(hours=-3))).date().isoformat()

PRECIO_MIN_PLAUSIBLE = 3_000_000
PRECIO_MAX_PLAUSIBLE = 40_000_000

# Si no hay avisos suficientes, se reintenta en la misma corrida antes de
# avisar por correo (muchos bloqueos de Cloudflare son temporales y se
# resuelven solos en un rato).
MAX_REINTENTOS = 3
ESPERA_REINTENTO_MIN = 5

# Si el precio calculado hoy se aleja mas de esto (en %) del valor del dia
# anterior para la misma categoria, se trata como sospechoso: no se publica
# y se reintenta como si no hubiera habido avisos suficientes.
VARIACION_MAX_PORCENTAJE = 0.20
CLAVES_CON_CONTROL_VARIACION = ["manual", "automatica", "maximo"]

# JS que corre DENTRO de la pagina. Devuelve lista de {precio, transmision, href}.
# linkPattern decide que prefijo de href cuenta como "el link de un aviso".
EXTRAER_JS = """
(linkPattern) => {
  function ownText(el) {
    let t = '';
    for (const node of el.childNodes) { if (node.nodeType === 3) t += node.textContent; }
    return t.trim();
  }
  // Chileautos: el link <a> es DESCENDIENTE del bloque de la tarjeta.
  // Yapo: el link <a> ES el bloque entero de la tarjeta.
  // hrefOf cubre ambos casos, probado contra los dos sitios en vivo.
  function hrefOf(el, linkPattern) {
    if (el.tagName === 'A') {
      const h = el.getAttribute('href');
      if (h && h.includes(linkPattern)) return h;
    }
    if (el.querySelectorAll) {
      const links = Array.from(el.querySelectorAll('a[href*="' + linkPattern + '"]'));
      if (links.length === 1) return links[0].getAttribute('href');
    }
    return null;
  }
  const re = /^\\$\\s?[\\d.]{7,12}$/;
  const all = Array.from(document.querySelectorAll('span, div'));
  const priceEls = all.filter(el => re.test(ownText(el)));
  const avisos = [];
  const seen = new Set();
  for (const span of priceEls) {
    let el = span;
    let href = null;
    for (let i = 0; i < 12 && el; i++) {
      href = hrefOf(el, linkPattern);
      if (href) break;
      el = el.parentElement;
    }
    if (!href || seen.has(href)) continue;
    seen.add(href);
    const cardText = el.innerText;
    const precio = parseInt(ownText(span).replace(/[$.\\s]/g, ''), 10);
    let transmision = null;
    if (/\\bManual\\b/.test(cardText)) transmision = 'manual';
    else if (/\\bAutom[a\\u00e1]tica\\b/.test(cardText)) transmision = 'automatica';
    const yearMatch = cardText.match(/\\b(201[5-9]|202[0-6])\\b/);
    const anio = yearMatch ? yearMatch[1] : null;
    avisos.push({precio, transmision, href, anio, texto: cardText});
  }
  return avisos;
}
"""


def _filtrar_plausibles(avisos):
    return [a for a in avisos if PRECIO_MIN_PLAUSIBLE <= a["precio"] <= PRECIO_MAX_PLAUSIBLE]


def _filtrar_palabra_obligatoria(avisos, palabra_obligatoria):
    """Descarta avisos cuyo texto completo de la tarjeta no menciona la
    palabra obligatoria del modelo (ej. "fronx"). Sin este filtro, un
    aviso de otro modelo que aparezca mezclado en los resultados de
    busqueda se cuenta igual -- esto corrige ese bug (modelos.json ya
    traia esta palabra configurada, pero el scraper nunca la usaba)."""
    if not palabra_obligatoria:
        return avisos
    palabra = palabra_obligatoria.lower()
    return [a for a in avisos if palabra in a.get("texto", "").lower()]


def _deduplicar_cross_source(avisos_chile, avisos_yapo):
    """Heuristica conservadora para no contar dos veces el mismo vehiculo
    si el mismo vendedor lo publico en Chileautos y en Yapo (practica
    comun en Chile, sobre todo de concesionarios): si un aviso de Yapo
    tiene exactamente el mismo precio, año y transmision que uno de
    Chileautos, se asume que es el mismo auto y se descarta el de Yapo.

    Limite conocido: esto NO detecta duplicados si el vendedor publico
    precios distintos en cada sitio, porque hoy el scraper no lee
    kilometraje, version ni ubicacion (los campos que permitirian un
    match mas fino). Es deliberadamente conservador: prefiere dejar pasar
    un duplicado raro antes que descartar por error dos autos distintos
    que coinciden en precio/año/transmision por casualidad.
    """
    firmas_chile = {(a["precio"], a.get("anio"), a.get("transmision")) for a in avisos_chile}
    yapo_filtrado = []
    duplicados = 0
    for a in avisos_yapo:
        firma = (a["precio"], a.get("anio"), a.get("transmision"))
        if firma in firmas_chile:
            duplicados += 1
            continue
        yapo_filtrado.append(a)
    return avisos_chile, yapo_filtrado, duplicados


def _variacion_sospechosa(categorias_nuevas, categorias_anteriores):
    """Compara las categorias recien calculadas contra las del dia anterior.
    Devuelve una lista de (categoria, valor_anterior, valor_nuevo, variacion)
    para las que cambiaron mas de VARIACION_MAX_PORCENTAJE. Si no hay valor
    anterior para comparar (primera corrida, o esa categoria no existia
    antes), esa categoria simplemente no se reporta -- no es sospechosa por
    falta de dato previo."""
    sospechosos = []
    if not categorias_anteriores:
        return sospechosos
    for clave in CLAVES_CON_CONTROL_VARIACION:
        anterior = categorias_anteriores.get(clave)
        nuevo = categorias_nuevas.get(clave)
        if anterior is None or nuevo is None or anterior == 0:
            continue
        variacion = abs(nuevo - anterior) / anterior
        if variacion > VARIACION_MAX_PORCENTAJE:
            sospechosos.append((clave, anterior, nuevo, variacion))
    return sospechosos


def _esperar_cloudflare(page, intentos=6, espera_ms=1500):
    """Si Cloudflare muestra la pagina intermedia "Just a moment...",
    espera a que termine su verificacion automatica (normalmente toma unos
    segundos) en vez de seguir de inmediato. No hace nada si la pagina ya
    cargo normal."""
    for _ in range(intentos):
        titulo = (page.title() or "").lower()
        if "just a moment" not in titulo and "moment" not in titulo:
            return
        page.wait_for_timeout(espera_ms)


def _diagnosticar_pagina_vacia(page, nombre_sitio):
    """Si no se encontro ningun aviso, imprime pistas sobre por que: titulo
    de la pagina y un fragmento del texto visible. Esto ayuda a distinguir
    un bloqueo anti-bot (Cloudflare, "verifica que eres humano", etc.) de
    un simple cambio de estructura del sitio."""
    try:
        titulo = page.title()
        texto = page.evaluate("document.body ? document.body.innerText.slice(0, 300) : ''")
        print(f"  DIAGNOSTICO {nombre_sitio}: titulo='{titulo}'")
        print(f"  DIAGNOSTICO {nombre_sitio}: primeros 300 caracteres del body:")
        print(f"    {texto!r}")
    except Exception as e:
        print(f"  DIAGNOSTICO {nombre_sitio}: no se pudo inspeccionar la pagina: {e}")


def extraer_avisos_chileautos(page, marca, modelo, anio, palabra_obligatoria=None):
    url = f"https://www.chileautos.cl/vehiculos/usado-tipo/{marca}/{modelo}/{anio}-ano/?sort=~Price"
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    _esperar_cloudflare(page)
    avisos = page.evaluate(EXTRAER_JS, "/vehiculos/detalles/")
    avisos = _filtrar_palabra_obligatoria(avisos, palabra_obligatoria)
    avisos = _filtrar_plausibles(avisos)
    if not avisos:
        _diagnosticar_pagina_vacia(page, "Chileautos")
    return avisos


def extraer_avisos_yapo(page, marca, modelo, anio, palabra_obligatoria=None):
    # A diferencia de Chileautos, la URL de Yapo no filtra por anio (busca
    # el modelo completo, mezclando todos los anios). Por eso filtramos
    # aqui comparando el anio leido de cada aviso contra el anio pedido.
    url = f"https://www.yapo.cl/autos-usados/{marca}/{modelo}"
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)  # Yapo carga los avisos via JS, necesita tiempo extra
    _esperar_cloudflare(page)
    avisos = page.evaluate(EXTRAER_JS, "/autos-usados/")
    avisos = [a for a in avisos if a.get("anio") == str(anio)]
    avisos = _filtrar_palabra_obligatoria(avisos, palabra_obligatoria)
    avisos = _filtrar_plausibles(avisos)
    if not avisos:
        _diagnosticar_pagina_vacia(page, "Yapo")
    return avisos


def calcular_categorias(avisos, min_avisos_validos):
    """A partir de la lista combinada de avisos, calcula las 5 categorias.
    Devuelve None si no hay suficientes avisos (en vez de inventar datos)."""
    if len(avisos) < min_avisos_validos:
        return None

    precios_todos = sorted(a["precio"] for a in avisos)
    precios_manual = sorted(a["precio"] for a in avisos if a["transmision"] == "manual")
    precios_auto = sorted(a["precio"] for a in avisos if a["transmision"] == "automatica")

    resultado = {}
    if precios_manual:
        resultado["manual"] = precios_manual[0]
        resultado["manual_fuente"] = "avisos_manual"
    else:
        resultado["manual"] = precios_todos[0]
        resultado["manual_fuente"] = "aproximado_minimo_general"

    if precios_auto:
        resultado["automatica"] = precios_auto[0]
        resultado["automatica_fuente"] = "avisos_automatica"
    elif len(precios_todos) >= 2:
        resultado["automatica"] = precios_todos[1]
        resultado["automatica_fuente"] = "aproximado_segundo_general"

    resultado["maximo"] = precios_todos[-1]
    resultado["nuevo"] = int(round(resultado["maximo"] * 1.10))
    resultado["nuevo_bono"] = int(round(resultado["manual"] * 1.01))
    resultado["total_avisos"] = len(avisos)
    resultado["fecha"] = HOY
    return resultado


def main():
    os.makedirs(DATA, exist_ok=True)
    cfg = json.load(open(CONFIG, encoding="utf-8"))
    min_avisos = cfg.get("min_avisos_validos", 2)
    # Minimo exigido POR FUENTE (antes solo se exigia el total combinado,
    # lo que permitia que una sola fuente definiera el precio si la otra
    # fallaba -- la regla del proyecto es usar siempre ambas fuentes).
    min_avisos_por_fuente = cfg.get("min_avisos_por_fuente", min_avisos)
    ultimo = json.load(open(ULTIMO, encoding="utf-8")) if os.path.exists(ULTIMO) else {}

    exit_code = 0

    with sync_playwright() as p:
        # Chileautos y Yapo usan Cloudflare para bloquear navegadores "robot".
        # Estos flags y el script de abajo hacen que el navegador headless se
        # parezca mas a uno real (el detector de Cloudflare mira sobre todo
        # navigator.webdriver, el modo headless real, y el idioma/zona horaria).
        browser = p.chromium.launch(
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="es-CL",
            timezone_id="America/Santiago",
        )
        page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
        )

        for mod in cfg["modelos"]:
            for anio in mod["anios"]:
                clave = f"{mod['id']}|{anio}"
                print(f"\n[{clave}]")
                palabra_obligatoria = mod.get("palabra_obligatoria")
                categorias_anteriores = ultimo.get(clave)

                categorias = None
                motivo_falla = None
                for intento in range(1, MAX_REINTENTOS + 1):
                    print(f"  Intento {intento}/{MAX_REINTENTOS}...")

                    try:
                        avisos_chile = extraer_avisos_chileautos(
                            page, mod["marca"], mod["modelo"], anio, palabra_obligatoria
                        )
                    except Exception as e:
                        print(f"  ERROR Chileautos: {e}")
                        avisos_chile = []

                    try:
                        avisos_yapo = extraer_avisos_yapo(
                            page, mod["marca"], mod["modelo"], anio, palabra_obligatoria
                        )
                    except Exception as e:
                        print(f"  ERROR Yapo: {e}")
                        avisos_yapo = []

                    avisos_chile, avisos_yapo, duplicados = _deduplicar_cross_source(avisos_chile, avisos_yapo)
                    if duplicados:
                        print(f"  {duplicados} aviso(s) de Yapo descartado(s) por probable duplicado de Chileautos")

                    print(f"  Chileautos: {len(avisos_chile)} avisos | Yapo: {len(avisos_yapo)} avisos")

                    if len(avisos_chile) < min_avisos_por_fuente or len(avisos_yapo) < min_avisos_por_fuente:
                        categorias = None
                        motivo_falla = (
                            f"avisos insuficientes por fuente (minimo {min_avisos_por_fuente} cada una): "
                            f"Chileautos {len(avisos_chile)}, Yapo {len(avisos_yapo)}"
                        )
                    else:
                        todos = avisos_chile + avisos_yapo
                        categorias = calcular_categorias(todos, min_avisos)
                        if categorias is None:
                            motivo_falla = f"solo {len(todos)} avisos validos en total (minimo {min_avisos})"
                        else:
                            sospechosos = _variacion_sospechosa(categorias, categorias_anteriores)
                            if sospechosos:
                                detalle = ", ".join(
                                    f"{c}: ${a:,} -> ${n:,} ({v:.0%})" for c, a, n, v in sospechosos
                                )
                                print(f"  VARIACION SOSPECHOSA (>{VARIACION_MAX_PORCENTAJE:.0%}): {detalle}")
                                categorias = None
                                motivo_falla = f"variacion sospechosa respecto de ayer: {detalle}"

                    if categorias is not None:
                        break

                    if intento < MAX_REINTENTOS:
                        print(f"  {motivo_falla}. Reintentando en {ESPERA_REINTENTO_MIN} minutos...")
                        page.wait_for_timeout(ESPERA_REINTENTO_MIN * 60 * 1000)

                if categorias is None:
                    print(f"  SIN ACTUALIZAR tras {MAX_REINTENTOS} intentos: {motivo_falla}. Se mantiene el valor anterior.")
                    exit_code = 1
                    url_articulo = UNIDAD_BASE_URL + mod.get("articulo", "")
                    enviar_alerta(
                        asunto=f"Precios Fronx: no se pudo actualizar {clave} - {url_articulo}",
                        cuerpo=(
                            f"El script de precios no pudo actualizar {clave} hoy ({HOY}), "
                            f"despues de {MAX_REINTENTOS} intentos separados por "
                            f"{ESPERA_REINTENTO_MIN} minutos cada uno.\n\n"
                            f"Motivo: {motivo_falla}\n\n"
                            f"Se mantuvo el ultimo precio valido. Articulo: {url_articulo}"
                        ),
                    )
                    continue

                ultimo[clave] = categorias
                print(
                    f"  OK manual=${categorias['manual']:,} "
                    f"automatica=${categorias.get('automatica', 0):,} "
                    f"maximo=${categorias['maximo']:,}"
                )

        browser.close()

    json.dump(ultimo, open(ULTIMO, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nGuardado en {ULTIMO}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
