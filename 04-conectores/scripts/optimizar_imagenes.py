#!/usr/bin/env python3
"""
Optimizador de imagenes para web (Webflow / landing) — Unidad Creditos.

Toma una o varias imagenes de origen (PNG/JPG generadas por IA, fotos, mockups)
y genera versiones listas para produccion: redimensionadas a anchos responsive,
recomprimidas y exportadas en WebP (principal) + JPG (fallback). Pensado para
subir assets livianos a Webflow sin perder nitidez.

Requisito: Pillow  ->  pip install -r requirements.txt   (o: pip install Pillow)

Uso:
  # Un archivo, presets desktop + mobile (por defecto):
  python 04-conectores/scripts/optimizar_imagenes.py assets/unidad-hero-ejecutiva-desktop.png

  # Varias imagenes a la vez:
  python 04-conectores/scripts/optimizar_imagenes.py assets/hero1.png assets/hero2.png

  # Carpeta de salida y anchos personalizados:
  python 04-conectores/scripts/optimizar_imagenes.py img.png --out assets/web --anchos 1920 1280 768 480

  # Solo WebP, calidad 80:
  python 04-conectores/scripts/optimizar_imagenes.py img.png --formatos webp --calidad 80

  # Quitar el fondo (recorte transparente) + exportar PNG/WebP con alfa:
  python 04-conectores/scripts/optimizar_imagenes.py ejecutiva.png --quitar-fondo --formatos webp png

Presets de ancho:
  desktop -> 1920, 1280        mobile -> 768, 480        ambos (default) -> los 4

Quitar fondo (--quitar-fondo): usa 'rembg' (segmentacion con modelo U2Net) para
recortar el sujeto y dejar fondo transparente. Requiere:  pip install rembg onnxruntime
(la 1a vez descarga el modelo ~170 MB). Ideal para fotos de personas (pelo incluido).
Al usarlo, exporta solo en formatos con alfa (webp/png); el JPG se omite.

Por que Python + Pillow: redimensionar/recomprimir es un trabajo puntual de
glue-code; Pillow lo resuelve en pocas lineas y es el estandar del ecosistema.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit(
        "Falta Pillow. Instalalo con:\n"
        "  pip install Pillow\n"
        "o  pip install -r requirements.txt"
    )

# --------------------------------------------------------------------------- #
# Configuracion
# --------------------------------------------------------------------------- #

PRESETS_ANCHO = {
    "desktop": [1920, 1280],
    "mobile": [768, 480],
    "ambos": [1920, 1280, 768, 480],
}

FORMATOS_VALIDOS = {"webp", "jpg", "png"}
FORMATOS_CON_ALFA = {"webp", "png"}

# Sesion de rembg cacheada (cargar el modelo es costoso; se reutiliza).
_REMBG_SESSION = None


def _quitar_fondo(img: "Image.Image") -> "Image.Image":
    """Recorta el sujeto y devuelve la imagen en RGBA (fondo transparente).

    Usa rembg (modelo U2Net). Importacion perezosa para no exigir la
    dependencia cuando no se usa --quitar-fondo.
    """
    global _REMBG_SESSION
    try:
        from rembg import new_session, remove
    except ImportError:
        sys.exit(
            "Para --quitar-fondo necesitas 'rembg'. Instalalo con:\n"
            "  pip install rembg onnxruntime\n"
            "(la primera vez descarga el modelo ~170 MB)."
        )
    if _REMBG_SESSION is None:
        _REMBG_SESSION = new_session()
    recortada = remove(img.convert("RGBA"), session=_REMBG_SESSION)
    return recortada.convert("RGBA")


def _humano(num_bytes: float) -> str:
    """Tamano de archivo legible (B/KB/MB/GB)."""
    tam = float(num_bytes)
    for unidad in ("B", "KB", "MB"):
        if tam < 1024:
            return f"{tam:.0f} {unidad}" if unidad == "B" else f"{tam:.1f} {unidad}"
        tam /= 1024
    return f"{tam:.1f} GB"


def _exportar(img: Image.Image, destino: Path, formato: str, calidad: int) -> int:
    """Guarda la imagen en el formato pedido y devuelve el tamano en bytes."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    if formato == "webp":
        img.save(destino, "WEBP", quality=calidad, method=6)
    elif formato == "jpg":
        # JPG no soporta alfa: aplanar sobre blanco.
        if img.mode in ("RGBA", "LA", "P"):
            fondo = Image.new("RGB", img.size, (255, 255, 255))
            rgba = img.convert("RGBA")
            fondo.paste(rgba, mask=rgba.split()[-1])
            img = fondo
        img.convert("RGB").save(destino, "JPEG", quality=calidad, optimize=True, progressive=True)
    elif formato == "png":
        img.save(destino, "PNG", optimize=True)
    return destino.stat().st_size


def optimizar(
    origen: Path,
    out_dir: Path,
    anchos: list[int],
    formatos: list[str],
    calidad: int,
    quitar_fondo: bool = False,
) -> list[tuple[Path, int]]:
    """Genera todas las variantes (ancho x formato) de una imagen."""
    resultados: list[tuple[Path, int]] = []
    with Image.open(origen) as im:
        im = ImageOps.exif_transpose(im)  # respeta orientacion EXIF
        if quitar_fondo:
            im = _quitar_fondo(im)
        ancho_orig, alto_orig = im.size
        base = origen.stem

        for ancho in sorted(set(anchos), reverse=True):
            # No agrandar: si la fuente es mas chica, se usa su ancho real.
            destino_ancho = min(ancho, ancho_orig)
            if destino_ancho == ancho_orig:
                redim = im.copy()
            else:
                nuevo_alto = round(alto_orig * destino_ancho / ancho_orig)
                redim = im.resize((destino_ancho, nuevo_alto), Image.LANCZOS)

            for fmt in formatos:
                ext = "jpg" if fmt == "jpg" else fmt
                destino = out_dir / f"{base}-{destino_ancho}w.{ext}"
                tam = _exportar(redim, destino, fmt, calidad)
                resultados.append((destino, tam))
    return resultados


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Optimiza imagenes para web (responsive, WebP + JPG)."
    )
    parser.add_argument("imagenes", nargs="+", help="Rutas de las imagenes de origen.")
    parser.add_argument(
        "--out",
        default="assets/web",
        help="Carpeta de salida (default: assets/web).",
    )
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS_ANCHO),
        default="ambos",
        help="Preset de anchos: desktop, mobile o ambos (default: ambos).",
    )
    parser.add_argument(
        "--anchos",
        type=int,
        nargs="+",
        help="Anchos en px (sobreescribe --preset). Ej: --anchos 1920 1280 768 480",
    )
    parser.add_argument(
        "--formatos",
        nargs="+",
        default=["webp", "jpg"],
        help="Formatos de salida: webp jpg png (default: webp jpg).",
    )
    parser.add_argument(
        "--calidad",
        type=int,
        default=82,
        help="Calidad de compresion 1-100 (default: 82).",
    )
    parser.add_argument(
        "--quitar-fondo",
        action="store_true",
        help="Recorta el sujeto (fondo transparente) con rembg. Fuerza formatos con alfa.",
    )
    args = parser.parse_args(argv)

    formatos = [f.lower() for f in args.formatos]
    invalidos = set(formatos) - FORMATOS_VALIDOS
    if invalidos:
        parser.error(f"Formato(s) no soportado(s): {', '.join(invalidos)}")

    if args.quitar_fondo:
        # Con recorte transparente, el JPG no sirve (aplana el alfa): se omite.
        descartados = [f for f in formatos if f not in FORMATOS_CON_ALFA]
        formatos = [f for f in formatos if f in FORMATOS_CON_ALFA] or ["png"]
        if descartados:
            print(
                f"  i --quitar-fondo: omito {', '.join(descartados)} "
                f"(no soportan transparencia). Uso: {', '.join(formatos)}."
            )

    anchos = args.anchos if args.anchos else PRESETS_ANCHO[args.preset]
    out_dir = Path(args.out)

    total_origen = 0
    total_salida = 0
    generados = 0

    for ruta in args.imagenes:
        origen = Path(ruta)
        if not origen.exists():
            print(f"  ! No existe: {origen}", file=sys.stderr)
            continue
        tam_origen = origen.stat().st_size
        total_origen += tam_origen
        print(f"\n{origen.name}  ({_humano(tam_origen)})")
        for destino, tam in optimizar(
            origen, out_dir, anchos, formatos, args.calidad, args.quitar_fondo
        ):
            total_salida += tam
            generados += 1
            print(f"   -> {destino}  ({_humano(tam)})")

    print(f"\nListo: {generados} archivos en '{out_dir}/'.")
    if total_origen and generados:
        print(
            f"Origen total: {_humano(total_origen)}  ->  "
            f"salida total: {_humano(total_salida)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
