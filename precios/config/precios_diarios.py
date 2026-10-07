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

HOY = datetime.now(timezone(timedelta(hours=-3))).date().isoformat()

PRECIO_MIN_PLAUSIBLE = 3_000_000
PRECIO_MAX_PLAUSIBLE = 40_000_000

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
    avisos.push({precio, transmision, href, anio});
  }
  return avisos;
}
"""


def _filtrar_plausibles(avisos):
    return [a for a in avisos if PRECIO_MIN_PLAUSIBLE <= a["precio"] <= PRECIO_MAX_PLAUSIBLE]


def extraer_avisos_chileautos(page, marca, modelo, anio):
    url = f"https://www.chileautos.cl/vehiculos/usado-tipo/{marca}/{modelo}/{anio}-ano/?sort=~Price"
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    avisos = page.evaluate(EXTRAER_JS, "/vehiculos/detalles/")
    return _filtrar_plausibles(avisos)


def extraer_avisos_yapo(page, marca, modelo, anio):
    # A diferencia de Chileautos, la URL de Yapo no filtra por anio (busca
    # el modelo completo, mezclando todos los anios). Por eso filtramos
    # aqui comparando el anio leido de cada aviso contra el anio pedido.
    url = f"https://www.yapo.cl/autos-usados/{marca}/{modelo}"
    page.goto(url, timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)  # Yapo carga los avisos via JS, necesita tiempo extra
    avisos = page.evaluate(EXTRAER_JS, "/autos-usados/")
    avisos = [a for a in avisos if a.get("anio") == str(anio)]
    return _filtrar_plausibles(avisos)


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
    ultimo = json.load(open(ULTIMO, encoding="utf-8")) if os.path.exists(ULTIMO) else {}

    exit_code = 0

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )

        for mod in cfg["modelos"]:
            for anio in mod["anios"]:
                clave = f"{mod['id']}|{anio}"
                print(f"\n[{clave}]")

                try:
                    avisos_chile = extraer_avisos_chileautos(page, mod["marca"], mod["modelo"], anio)
                except Exception as e:
                    print(f"  ERROR Chileautos: {e}")
                    avisos_chile = []

                try:
                    avisos_yapo = extraer_avisos_yapo(page, mod["marca"], mod["modelo"], anio)
                except Exception as e:
                    print(f"  ERROR Yapo: {e}")
                    avisos_yapo = []

                print(f"  Chileautos: {len(avisos_chile)} avisos | Yapo: {len(avisos_yapo)} avisos")

                todos = avisos_chile + avisos_yapo
                categorias = calcular_categorias(todos, min_avisos)

                if categorias is None:
                    print(f"  SIN ACTUALIZAR: solo {len(todos)} avisos validos (minimo {min_avisos}). Se mantiene el valor anterior.")
                    exit_code = 1
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
