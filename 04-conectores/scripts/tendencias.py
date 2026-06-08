#!/usr/bin/env python3
"""
Agregador de tendencias multi-fuente (propio, gratis) para Unidad Creditos.

Alternativa sin costo a trendsmcp.ai. Consulta directo el origen de cada senial,
usando solo la biblioteca estandar (sin API keys ni dependencias de pago):

  - google_trends_daily : tendencias de busqueda del dia en Chile (RSS oficial)
  - google_news         : volumen y titulares de noticias por keyword (RSS, es-CL)
  - wikipedia_pageviews : vistas de articulos de Wikipedia (REST API oficial)
  - pytrends (OPCIONAL) : interes en el tiempo por keyword (si esta instalado)

Cada conector falla de forma aislada: si una fuente no responde, las demas siguen.

Uso:
  python 04-conectores/scripts/tendencias.py                  # informe completo
  python 04-conectores/scripts/tendencias.py --fuentes news    # solo noticias
  python 04-conectores/scripts/tendencias.py --dias 14
  python 04-conectores/scripts/tendencias.py --md informe.md --json datos.json
  python 04-conectores/scripts/tendencias.py --keywords "crédito automotriz" "comprar auto usado"

Por que Python y no Rust: este trabajo es glue-code (HTTP + parseo + JSON) que
itera rapido y aprovecha un ecosistema enorme. Rust solo convendria para un
daemon de alto rendimiento o un binario distribuible, que aqui no se necesita.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

# --------------------------------------------------------------------------- #
# Configuracion por defecto (editable o via --keywords / --wiki)
# --------------------------------------------------------------------------- #

KEYWORDS = [
    "crédito automotriz",
    "crédito automotriz entre particulares",
    "comprar auto usado",
    "crédito sin acreditar ingresos",
    "precio bencina",
    "permiso de circulación",
    "restricción vehicular",
]

# Articulos de Wikipedia (es) como proxy de interes en modelos/marcas/temas.
WIKI_ARTICULOS = [
    "Hyundai_Tucson",
    "Suzuki_Swift",
    "Tesla,_Inc.",
    "Automóvil",
]

# Para resaltar relevancia en el trending diario.
KEYWORDS_RELEVANTES = [
    "auto", "vehic", "veh\u00edc", "camioneta", "suv", "moto",
    "credit", "cr\u00e9dit", "financ", "prenda", "leasing", "cuota",
    "bencina", "combustible", "petr", "diesel", "gasolina", "enap",
    "restric", "permiso de circ", "patente", "transfer",
    "utm", "uf", "multa", "tr\u00e1nsito", "transito",
    "tasa", "banco", "cmf", "seguro automotriz",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36 "
    "(UnidadCreditos-TrendsBot; contacto: skalling.com)"
)


# --------------------------------------------------------------------------- #
# HTTP utilitario (reintentos + gzip)
# --------------------------------------------------------------------------- #

def http_get(url, intentos=3, timeout=30):
    ultimo = None
    headers = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"}
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
                return data
        except Exception as exc:  # noqa: BLE001
            ultimo = exc
            if i < intentos - 1:
                time.sleep(1.5 * (i + 1))
    raise RuntimeError("fallo HTTP (%s): %s" % (url, ultimo))


def es_relevante(texto):
    t = (texto or "").lower()
    return any(kw in t for kw in KEYWORDS_RELEVANTES)


# --------------------------------------------------------------------------- #
# Conector 1: Google Trends - trending diario de Chile (RSS)
# --------------------------------------------------------------------------- #

def google_trends_daily(geo="CL"):
    ns = {"ht": "https://trends.google.com/trending/rss"}
    url = "https://trends.google.com/trending/rss?geo=%s" % geo
    root = ET.fromstring(http_get(url))
    items = []
    for it in root.iter("item"):
        titulo = (it.findtext("title") or "").strip()
        traf = (it.findtext("ht:approx_traffic", namespaces=ns) or "").strip()
        noticias = [
            (n.findtext("ht:news_item_title", namespaces=ns) or "").strip()
            for n in it.findall("ht:news_item", namespaces=ns)
        ]
        rel = es_relevante(titulo) or any(es_relevante(x) for x in noticias)
        items.append({
            "termino": titulo,
            "trafico": traf,
            "relevante": rel,
            "noticias": [x for x in noticias if x][:2],
        })
    return {"fuente": "google_trends_daily", "geo": geo, "items": items}


# --------------------------------------------------------------------------- #
# Conector 2: Google News - volumen/titulares por keyword (RSS es-CL)
# --------------------------------------------------------------------------- #

def google_news(keyword, dias=7, hl="es-CL", gl="CL", ceid="CL:es"):
    q = urllib.parse.quote(keyword)
    url = ("https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s"
           % (q, hl, gl, urllib.parse.quote(ceid)))
    root = ET.fromstring(http_get(url))
    corte = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=dias)
    articulos = []
    for it in root.iter("item"):
        titulo = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        fecha = (it.findtext("pubDate") or "").strip()
        fuente_el = it.find("source")
        fuente = fuente_el.text.strip() if fuente_el is not None and fuente_el.text else ""
        ts = _parse_rss_date(fecha)
        if ts and ts < corte:
            continue
        articulos.append({"titulo": titulo, "url": link, "fuente": fuente, "fecha": fecha})
    return {
        "fuente": "google_news",
        "keyword": keyword,
        "dias": dias,
        "volumen": len(articulos),     # proxy de momentum noticioso
        "articulos": articulos[:8],
    }


def _parse_rss_date(s):
    if not s:
        return None
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            d = dt.datetime.strptime(s, fmt)
            if d.tzinfo is None:
                d = d.replace(tzinfo=dt.timezone.utc)
            return d
        except ValueError:
            continue
    return None


# --------------------------------------------------------------------------- #
# Conector 3: Wikipedia pageviews (REST API oficial, gratis)
# --------------------------------------------------------------------------- #

def wikipedia_pageviews(articulo, dias=30, proyecto="es.wikipedia"):
    hoy = dt.date.today()
    inicio = hoy - dt.timedelta(days=dias)
    art = urllib.parse.quote(articulo, safe="")
    url = (
        "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        "%s/all-access/all-agents/%s/daily/%s/%s"
        % (proyecto, art, inicio.strftime("%Y%m%d"), hoy.strftime("%Y%m%d"))
    )
    data = json.loads(http_get(url))
    serie = [(i["timestamp"][:8], i["views"]) for i in data.get("items", [])]
    total = sum(v for _, v in serie)
    # momentum: ultimos 7 dias vs 7 previos
    ult7 = sum(v for _, v in serie[-7:])
    prev7 = sum(v for _, v in serie[-14:-7]) or 0
    crecimiento = None
    if prev7:
        crecimiento = round((ult7 - prev7) / prev7 * 100, 1)
    return {
        "fuente": "wikipedia_pageviews",
        "articulo": articulo,
        "dias": dias,
        "vistas_total": total,
        "vistas_ult7": ult7,
        "crecimiento_pct_7d": crecimiento,
        "serie": serie,
    }


# --------------------------------------------------------------------------- #
# Conector 4 (OPCIONAL): pytrends - interes en el tiempo por keyword
# --------------------------------------------------------------------------- #

def pytrends_interes(keywords, geo="CL", timeframe="today 3-m"):
    try:
        from pytrends.request import TrendReq  # type: ignore
    except Exception:  # noqa: BLE001
        return {"fuente": "pytrends", "disponible": False,
                "nota": "pytrends no instalado. Opcional: pip install pytrends"}
    try:
        py = TrendReq(hl="es-CL", tz=180)
        py.build_payload(keywords[:5], geo=geo, timeframe=timeframe)
        df = py.interest_over_time()
        resultados = []
        for kw in keywords[:5]:
            if kw in df.columns:
                serie = df[kw].tolist()
                resultados.append({
                    "keyword": kw,
                    "ultimo": int(serie[-1]) if serie else None,
                    "promedio": round(sum(serie) / len(serie), 1) if serie else None,
                })
        return {"fuente": "pytrends", "disponible": True, "geo": geo,
                "timeframe": timeframe, "resultados": resultados}
    except Exception as exc:  # noqa: BLE001
        return {"fuente": "pytrends", "disponible": False, "error": str(exc)}


# --------------------------------------------------------------------------- #
# Orquestacion + informe
# --------------------------------------------------------------------------- #

def correr(fuentes, keywords, wiki, dias, usar_pytrends):
    out = {"generado": dt.datetime.now().isoformat(timespec="seconds"), "datos": {}}

    if "daily" in fuentes:
        out["datos"]["google_trends_daily"] = _safe(google_trends_daily)

    if "news" in fuentes:
        noticias = []
        for kw in keywords:
            noticias.append(_safe(google_news, kw, dias))
        noticias = [n for n in noticias if n]
        noticias.sort(key=lambda x: x.get("volumen", 0), reverse=True)
        out["datos"]["google_news"] = noticias

    if "wikipedia" in fuentes:
        # Wikipedia necesita >=14 dias para calcular momentum (7d vs 7d previos).
        win_wiki = max(dias, 30)
        wikis = [_safe(wikipedia_pageviews, a, win_wiki) for a in wiki]
        wikis = [w for w in wikis if w]
        wikis.sort(key=lambda x: x.get("crecimiento_pct_7d") or -999, reverse=True)
        out["datos"]["wikipedia_pageviews"] = wikis

    if usar_pytrends:
        out["datos"]["pytrends"] = _safe(pytrends_interes, keywords) or {}

    return out


def _safe(fn, *args):
    try:
        return fn(*args)
    except Exception as exc:  # noqa: BLE001
        print("  ! %s fallo: %s" % (fn.__name__, exc), file=sys.stderr)
        return None


def a_markdown(out):
    L = []
    L.append("# Informe de tendencias — Unidad Créditos")
    L.append("> Generado: %s · Fuentes propias (gratis)\n" % out["generado"])
    d = out["datos"]

    if "google_news" in d:
        L.append("## Momentum noticioso por keyword (Google News, es-CL)")
        L.append("| Keyword | Noticias recientes |")
        L.append("|---|---|")
        for n in d["google_news"]:
            L.append("| %s | %d |" % (n["keyword"], n["volumen"]))
        L.append("")
        top = d["google_news"][0] if d["google_news"] else None
        if top and top["articulos"]:
            L.append("### Titulares destacados de \"%s\"" % top["keyword"])
            for a in top["articulos"][:5]:
                L.append("- %s (%s)" % (a["titulo"], a["fuente"]))
                if a["url"]:
                    L.append("  %s" % a["url"])
            L.append("")

    if "wikipedia_pageviews" in d:
        L.append("## Interés en Wikipedia (vistas, últimos %dd)" % (d["wikipedia_pageviews"][0]["dias"] if d["wikipedia_pageviews"] else 30))
        L.append("| Artículo | Vistas total | Últimos 7d | Δ vs 7d previos |")
        L.append("|---|---|---|---|")
        for w in d["wikipedia_pageviews"]:
            cre = "n/d" if w["crecimiento_pct_7d"] is None else ("%+.1f%%" % w["crecimiento_pct_7d"])
            L.append("| %s | %s | %s | %s |" % (w["articulo"], w["vistas_total"], w["vistas_ult7"], cre))
        L.append("")

    if "google_trends_daily" in d and d["google_trends_daily"]:
        rel = [i for i in d["google_trends_daily"]["items"] if i["relevante"]]
        L.append("## Trending diario en Chile (Google Trends)")
        L.append("Relevantes para autos/crédito: %d de %d" %
                 (len(rel), len(d["google_trends_daily"]["items"])))
        for i in rel:
            L.append("- ★ %s (%s)" % (i["termino"], i["trafico"]))
        L.append("")

    if "pytrends" in d and d["pytrends"]:
        p = d["pytrends"]
        L.append("## Interés en el tiempo (pytrends)")
        if not p.get("disponible"):
            L.append("- %s" % p.get("nota", p.get("error", "no disponible")))
        else:
            for r in p.get("resultados", []):
                L.append("- %s: último=%s, promedio=%s" %
                         (r["keyword"], r["ultimo"], r["promedio"]))
        L.append("")

    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Agregador de tendencias propio (gratis) para Unidad Creditos")
    ap.add_argument("--fuentes", nargs="+",
                    default=["daily", "news", "wikipedia"],
                    choices=["daily", "news", "wikipedia"],
                    help="conectores a usar (por defecto: daily news wikipedia)")
    ap.add_argument("--keywords", nargs="+", default=KEYWORDS, help="keywords a monitorear")
    ap.add_argument("--wiki", nargs="+", default=WIKI_ARTICULOS, help="articulos de Wikipedia (es)")
    ap.add_argument("--dias", type=int, default=7, help="ventana en dias (news) / 30 sugerido para wiki")
    ap.add_argument("--pytrends", action="store_true", help="incluir pytrends (requiere pip install pytrends)")
    ap.add_argument("--md", metavar="ARCHIVO", help="guardar informe markdown")
    ap.add_argument("--json", metavar="ARCHIVO", help="guardar datos crudos en JSON")
    args = ap.parse_args()

    # Consola de Windows suele ser cp1252; forzamos UTF-8 para imprimir acentos/simbolos.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass

    print("Consultando fuentes: %s ..." % ", ".join(args.fuentes), file=sys.stderr)
    out = correr(args.fuentes, args.keywords, args.wiki, args.dias, args.pytrends)

    md = a_markdown(out)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
        print("JSON guardado en %s" % args.json, file=sys.stderr)
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(md)
        print("Markdown guardado en %s" % args.md, file=sys.stderr)
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
