#!/usr/bin/env python3
"""
Extractor de Google Trends (Chile) para el agente de Research de Tendencias.

Lee el feed RSS de tendencias diarias de Google Trends para Chile, lo parsea
(sin dependencias externas) y resalta los terminos relevantes para Unidad Creditos
(autos, credito, bencina, transporte, normativa vehicular, etc.).

Uso:
    python scripts/trends_cl.py                # todo + resaltado relevante
    python scripts/trends_cl.py --solo-relevante
    python scripts/trends_cl.py --json salida.json
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

RSS_URL = "https://trends.google.com/trending/rss?geo=CL"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml,application/xml,text/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
}

KEYWORDS_RELEVANTES = [
    "auto", "autos", "vehic", "veh\u00edc", "camioneta", "suv", "moto",
    "credit", "cr\u00e9dit", "financ", "prenda", "leasing", "cuota",
    "bencina", "combustible", "petr", "diesel", "gasolina", "enap",
    "restric", "permiso de circ", "patente", "transfer",
    "utm", "uf", "multa", "tr\u00e1nsito", "transito", "revisi\u00f3n t\u00e9cnica",
    "tasa", "banco", "cmf", "seguro automotriz",
]

NS = {"ht": "https://trends.google.com/trending/rss"}


def fetch_rss(url=RSS_URL, intentos=3):
    ultimo_error = None
    for i in range(intentos):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
                return data
        except Exception as exc:  # noqa: BLE001
            ultimo_error = exc
            if i < intentos - 1:
                time.sleep(2 * (i + 1))
    raise RuntimeError(
        "No se pudo obtener el RSS tras %d intentos: %s. Abre manualmente %s"
        % (intentos, ultimo_error, url)
    )


def parse_trends(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        traffic = (item.findtext("ht:approx_traffic", namespaces=NS) or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        noticias = []
        for n in item.findall("ht:news_item", namespaces=NS):
            noticias.append({
                "titulo": (n.findtext("ht:news_item_title", namespaces=NS) or "").strip(),
                "url": (n.findtext("ht:news_item_url", namespaces=NS) or "").strip(),
                "fuente": (n.findtext("ht:news_item_source", namespaces=NS) or "").strip(),
            })
        items.append({
            "termino": title,
            "trafico_aprox": traffic,
            "fecha": pub,
            "relevante": es_relevante(title, noticias),
            "noticias": noticias,
        })
    return items


def es_relevante(titulo, noticias):
    texto = titulo.lower()
    for n in noticias:
        texto += " " + n.get("titulo", "").lower()
    return any(kw in texto for kw in KEYWORDS_RELEVANTES)


def imprimir(items, solo_relevante):
    relevantes = [i for i in items if i["relevante"]]
    print("Google Trends Chile -- %d tendencias (%d relevantes para autos/credito)\n"
          % (len(items), len(relevantes)))
    if relevantes:
        print("=== RELEVANTES PARA UNIDAD ===")
        for i in relevantes:
            _print_item(i)
        print()
    if not solo_relevante:
        print("=== TODAS LAS TENDENCIAS ===")
        for i in items:
            marca = "* " if i["relevante"] else "  "
            print("%s%7s  %s" % (marca, i["trafico_aprox"], i["termino"]))


def _print_item(i):
    print("* %s  (%s)  [%s]" % (i["termino"], i["trafico_aprox"], i["fecha"]))
    for n in i["noticias"][:2]:
        if n["titulo"]:
            print("    - %s (%s)" % (n["titulo"], n["fuente"]))
            if n["url"]:
                print("      %s" % n["url"])


def main():
    ap = argparse.ArgumentParser(
        description="Google Trends Chile para growth de Unidad Creditos")
    ap.add_argument("--solo-relevante", action="store_true",
                    help="muestra solo tendencias relevantes")
    ap.add_argument("--json", metavar="ARCHIVO",
                    help="guarda el resultado completo en JSON")
    args = ap.parse_args()
    try:
        xml_bytes = fetch_rss()
        items = parse_trends(xml_bytes)
    except Exception as exc:  # noqa: BLE001
        print("Error: %s" % exc, file=sys.stderr)
        return 1
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(items, fh, ensure_ascii=False, indent=2)
        print("Guardado en %s (%d tendencias)" % (args.json, len(items)))
    imprimir(items, args.solo_relevante)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
