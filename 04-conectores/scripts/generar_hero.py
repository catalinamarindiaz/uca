"""
Generador de mockups de hero — Unidad Crédito Automotriz
Produce variantes desktop (1280x700) y mobile (390x780) a partir de
los assets base del kit de ejecutiva.

Uso:
  python generar_hero.py

Salida: outputs/hero-variante-{slug}-desktop.png y -mobile.png
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

# ── Rutas (relativas al repo; no depender de una sesión específica) ──────────
BASE = Path(__file__).resolve().parents[2]
KIT_DESKTOP = BASE / "assets/web/kit/kit-ejecutiva-desktop-1024w.png"
KIT_MOBILE  = BASE / "assets/web/kit/kit-ejecutiva-mobile-480w.png"
OUT_DIR     = BASE / "assets/mockups"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Paleta UNIDAD ─────────────────────────────────────────────────────────────
NARANJA   = (230, 81,  0)       # naranja marca
AZUL_OSC  = (13,  28,  64)      # azul marino títulos
BLANCO    = (255, 255, 255)
GRIS_BG   = (245, 245, 243)
GRIS_TEXT = (90,  90,  90)
VERDE_OK  = (21, 128,  61)

# ── Fuentes ───────────────────────────────────────────────────────────────────
FONT_BOLD   = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Bold.otf"
FONT_REG    = "/usr/share/fonts/opentype/urw-base35/NimbusSans-Regular.otf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ── Helpers ───────────────────────────────────────────────────────────────────

def draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill)

def draw_text_wrapped(draw, text, x, y, max_width, fnt, fill, line_spacing=1.25):
    """Dibuja texto con wrap manual por píxeles."""
    words = text.split()
    lines, current = [], ""
    for w in words:
        test = (current + " " + w).strip()
        bbox = draw.textbbox((0, 0), test, font=fnt)
        if bbox[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)

    line_h = fnt.size * line_spacing
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=fnt, fill=fill)
    return y + len(lines) * line_h

def draw_check_item(draw, text, x, y, fnt):
    """Ítem con check verde."""
    draw.ellipse([x, y+2, x+16, y+18], fill=VERDE_OK)
    draw.text((x+4, y+1), "✓", font=ImageFont.truetype(FONT_BOLD, 12), fill=BLANCO)
    draw.text((x+24, y), text, font=fnt, fill=AZUL_OSC)

def badge(draw, text, x, y, fnt, bg=NARANJA, fg=BLANCO, radius=6, pad_x=14, pad_y=6):
    bbox = draw.textbbox((0,0), text, font=fnt)
    w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.rounded_rectangle([x, y, x+w+pad_x*2, y+h+pad_y*2], radius=radius, fill=bg)
    draw.text((x+pad_x, y+pad_y), text, font=fnt, fill=fg)
    return x + w + pad_x*2

def trust_strip(draw, items, y, canvas_w, fnt_sm):
    """Banda de trust badges horizontales centrada."""
    strip_w = canvas_w - 80
    col_w = strip_w // len(items)
    for i, (icon, label) in enumerate(items):
        cx = 40 + i * col_w + col_w // 2
        draw.text((cx - 10, y), icon, font=ImageFont.truetype(FONT_BOLD, 18), fill=NARANJA)
        draw_rounded_rect(draw, [cx-10, y-2, cx+14, y+20], 3, None)
        bbox = draw.textbbox((0,0), label, font=fnt_sm)
        lw = bbox[2]-bbox[0]
        draw.text((cx - lw//2 + 5, y+24), label, font=fnt_sm, fill=GRIS_TEXT)


# ── Variantes ─────────────────────────────────────────────────────────────────

VARIANTES = [
    {
        # VARIANTE A — Social proof como gancho de marca (recomendada)
        # El home debe presentar la marca, no el producto.
        # El problema es que nadie conoce UNIDAD todavía — la pregunta que
        # el usuario se hace al llegar es «¿puedo confiar en esto?».
        # Liderar con 1.750 reseñas y 4,9★ responde esa pregunta antes
        # que cualquier copy. El subtítulo introduce la amplitud de la marca
        # (automotoras + particulares) sin entrar en mecánica de producto.
        # El CTA dirige estratégicamente a entre particulares porque es
        # el producto diferenciador y el de mayor margen.
        "slug": "home-A-social-proof",
        "pagina": "/  (Home)",
        "h1_lines": ["4,9★ en Google.", "+1.760 opiniones reales.", "Así somos en UNIDAD."],
        "subtitulo": "Financiamos autos nuevos, usados y entre particulares. Proceso 100% digital, ejecutivas reales. Pie desde 20%, hasta 60 cuotas.",
        "cta": "Simula tu crédito entre particulares →",
        "checks": ["Pie desde 20% · hasta 60 cuotas", "Primera cuota hasta 60 días", "Proceso digital · ejecutiva real · sin filas"],
        "badge_txt": "4,9★ · +1.760 opiniones en Google",
    },
    {
        # VARIANTE B — Posicionamiento de marca (quiénes somos)
        # En vez de liderar con prueba social, lidera con identidad.
        # «Crédito automotriz 100% digital» es el claim de categoría que
        # diferencia a UNIDAD de los bancos (presenciales, lentos) y de
        # las automotoras (solo sus marcas). «Para comprar donde tú quieras»
        # amplía el alcance sin entrar en detalle — el usuario curioso
        # navega hacia productos, el listo va directo a simular.
        "slug": "home-B-posicionamiento",
        "pagina": "/  (Home)",
        "h1_lines": ["Crédito automotriz digital.", "Para automotoras", "y compras entre particulares."],
        "subtitulo": "Pie desde 20%, hasta 60 cuotas, primera cuota hasta 60 días. 4,9★ con más de 1.760 opiniones en Google.",
        "cta": "Simula tu crédito entre particulares →",
        "checks": ["Sin filas ni papeleos — todo online", "Ejecutiva experta te atiende en tiempo real", "Financiamos hasta el 80% del valor del auto"],
        "badge_txt": "4,9★ · +1.760 opiniones Google",
    },
    {
        # VARIANTE C — Benefit lead (outcome para el usuario)
        # En lugar de hablar de UNIDAD, habla del resultado del usuario.
        # «Tu próximo auto, financiado» es el deseo del visitante puesto
        # como promesa. «Rápido, digital, con alguien real» resuelve las
        # tres objeciones más comunes: ¿cuánto demora? ¿es online?
        # ¿hay un humano si algo falla? El subtítulo presenta la marca
        # y sus credenciales sin protagonismo excesivo.
        "slug": "home-C-benefit",
        "pagina": "/  (Home)",
        "h1_lines": ["Tu próximo auto, financiado.", "Rápido, digital y con", "alguien real que te apoya."],
        "subtitulo": "UNIDAD financia autos en automotoras y entre particulares. 4,9★ en Google · +500 automotoras preferentes · proceso 100% online.",
        "cta": "Simula tu crédito entre particulares →",
        "checks": ["Pie desde 20% · hasta 60 cuotas", "Financiamos hasta el 80% del auto", "Primera cuota hasta 60 días plazo"],
        "badge_txt": "4,9★ · +1.760 opiniones en Google",
    },
]


def make_desktop(v: dict) -> Path:
    W, H = 1280, 700
    canvas = Image.new("RGB", (W, H), BLANCO)
    draw = ImageDraw.Draw(canvas)

    # Fondo gris suave lado derecho
    draw.rectangle([W//2, 0, W, H], fill=GRIS_BG)

    # Barra naranja superior
    draw.rectangle([0, 0, W, 6], fill=NARANJA)

    # Logo placeholder
    fnt_logo = font(FONT_BOLD, 22)
    draw.text((40, 24), "unidad", font=fnt_logo, fill=NARANJA)
    draw.text((40, 48), "crédito automotriz", font=font(FONT_REG, 11), fill=GRIS_TEXT)

    # Nav placeholder
    nav_items = ["Tipos de crédito", "Nosotros", "Alianzas", "Blog", "Contacto"]
    nx = 220
    fnt_nav = font(FONT_REG, 12)
    for item in nav_items:
        draw.text((nx, 34), item, font=fnt_nav, fill=AZUL_OSC)
        bbox = draw.textbbox((0,0), item, font=fnt_nav)
        nx += bbox[2] - bbox[0] + 28
    # CTA nav
    badge(draw, "Paga tu cuenta", nx+10, 28, font(FONT_BOLD, 11),
          bg=AZUL_OSC, fg=BLANCO, pad_x=10, pad_y=6)

    # ── Columna izquierda: copy ───────────────────────────────────────────────
    left_x = 52
    text_max_w = 520

    # Badge de página
    badge(draw, v["pagina"], left_x, 95, font(FONT_REG, 11),
          bg=(230, 240, 255), fg=AZUL_OSC, radius=4, pad_x=10, pad_y=4)

    # H1 — auto-fit: reduce tamaño hasta que la línea más larga entre
    h1_size = 44
    while h1_size > 24:
        fnt_h1 = font(FONT_BOLD, h1_size)
        max_line_w = max(draw.textbbox((0,0), l, font=fnt_h1)[2] for l in v["h1_lines"])
        if max_line_w <= text_max_w:
            break
        h1_size -= 2
    y_h1 = 135
    for line in v["h1_lines"]:
        draw.text((left_x, y_h1), line, font=fnt_h1, fill=AZUL_OSC)
        y_h1 += int(h1_size * 1.25)

    # Subtítulo
    fnt_sub = font(FONT_REG, 16)
    y_sub = y_h1 + 12
    y_after_sub = draw_text_wrapped(draw, v["subtitulo"], left_x, y_sub,
                                     text_max_w, fnt_sub, GRIS_TEXT, 1.5)

    # Checks
    fnt_chk = font(FONT_REG, 14)
    y_chk = y_after_sub + 18
    for chk in v["checks"]:
        draw_check_item(draw, chk, left_x, y_chk, fnt_chk)
        y_chk += 28

    # CTA button
    y_cta = y_chk + 20
    fnt_cta = font(FONT_BOLD, 16)
    bbox = draw.textbbox((0,0), v["cta"], font=fnt_cta)
    btn_w = bbox[2] - bbox[0] + 48
    draw.rounded_rectangle([left_x, y_cta, left_x+btn_w, y_cta+48], radius=8, fill=NARANJA)
    draw.text((left_x+24, y_cta+14), v["cta"], font=fnt_cta, fill=BLANCO)

    # Trust badge
    badge_y = y_cta + 62
    fnt_badge = font(FONT_REG, 12)
    badge(draw, "⭐ " + v["badge_txt"], left_x, badge_y, fnt_badge,
          bg=(255, 248, 230), fg=(120, 80, 0), radius=6, pad_x=10, pad_y=5)

    # Disclaimer
    draw.text((left_x, H - 36), "Sujeto a evaluación. UNIDAD® nunca pide transferencias. unidadcreditos.cl",
              font=font(FONT_REG, 10), fill=GRIS_TEXT)

    # ── Columna derecha: ejecutiva ────────────────────────────────────────────
    eje = Image.open(KIT_DESKTOP).convert("RGBA")
    eje_h = int(H * 0.88)
    eje_w = int(eje.width * eje_h / eje.height)
    eje = eje.resize((eje_w, eje_h), Image.LANCZOS)

    # Pegar ejecutiva a la derecha
    eje_x = W - eje_w - 20
    canvas.paste(eje, (eje_x, H - eje_h), eje)

    # Burbuja flotante encima de ejecutiva
    bub_x, bub_y = W - 280, 90
    draw.rounded_rectangle([bub_x, bub_y, bub_x+230, bub_y+90], radius=12, fill=BLANCO)
    draw.rounded_rectangle([bub_x, bub_y, bub_x+230, bub_y+90], radius=12,
                           outline=NARANJA, width=2)
    draw.text((bub_x+14, bub_y+12), "📋 Simula en 1 minuto", font=font(FONT_BOLD, 13), fill=AZUL_OSC)
    draw.text((bub_x+14, bub_y+34), "Sin compromiso · 100% digital", font=font(FONT_REG, 11), fill=GRIS_TEXT)
    draw.text((bub_x+14, bub_y+56), "Ejecutiva real te responde", font=font(FONT_REG, 11), fill=GRIS_TEXT)

    out = OUT_DIR / f"hero-{v['slug']}-desktop.png"
    canvas.save(out, "PNG", optimize=True)
    return out


def make_mobile(v: dict) -> Path:
    W, H = 390, 780
    canvas = Image.new("RGB", (W, H), BLANCO)
    draw = ImageDraw.Draw(canvas)

    # Barra naranja
    draw.rectangle([0, 0, W, 5], fill=NARANJA)

    # Logo
    fnt_logo = font(FONT_BOLD, 18)
    draw.text((18, 16), "unidad  crédito automotriz", font=fnt_logo, fill=NARANJA)

    # Hamburger
    for dy in [0, 7, 14]:
        draw.rectangle([W-44, 16+dy, W-20, 18+dy], fill=AZUL_OSC)

    # Ejecutiva (mobile, portrait)
    eje = Image.open(KIT_MOBILE).convert("RGBA")
    eje_w = int(W * 0.52)
    eje_h = int(eje.height * eje_w / eje.width)
    eje = eje.resize((eje_w, eje_h), Image.LANCZOS)
    canvas.paste(eje, (W - eje_w, 48), eje)

    # Badge flotante sobre ejecutiva
    badge(draw, v["badge_txt"], 16, 58, font(FONT_BOLD, 10),
          bg=(255, 248, 230), fg=(120, 80, 0), radius=5, pad_x=8, pad_y=4)

    # H1
    fnt_h1 = font(FONT_BOLD, 30)
    y_h1 = 170
    for line in v["h1_lines"]:
        draw.text((16, y_h1), line, font=fnt_h1, fill=AZUL_OSC)
        y_h1 += 38

    # Subtítulo
    fnt_sub = font(FONT_REG, 14)
    y_sub = y_h1 + 8
    y_after = draw_text_wrapped(draw, v["subtitulo"], 16, y_sub, W-32, fnt_sub, GRIS_TEXT, 1.45)

    # Form placeholder
    form_y = y_after + 18
    draw.rounded_rectangle([16, form_y, W-16, form_y+42], radius=8,
                           outline=(200,200,200), fill=BLANCO, width=1)
    draw.text((28, form_y+13), "Nombre y Apellido", font=font(FONT_REG, 13), fill=(180,180,180))

    # CTA
    cta_y = form_y + 54
    fnt_cta = font(FONT_BOLD, 15)
    draw.rounded_rectangle([16, cta_y, W-16, cta_y+46], radius=8, fill=NARANJA)
    bbox = draw.textbbox((0,0), v["cta"], font=fnt_cta)
    tx = (W - (bbox[2]-bbox[0])) // 2
    draw.text((tx, cta_y+14), v["cta"], font=fnt_cta, fill=BLANCO)

    # Disclaimer
    draw.text((16, cta_y+58), "Sujeto a evaluación · unidadcreditos.cl", font=font(FONT_REG, 10), fill=GRIS_TEXT)

    # Trust strip
    t_y = cta_y + 82
    draw.line([16, t_y-4, W-16, t_y-4], fill=(220,220,220), width=1)
    trust_items = [("🏛", "+500 automotoras"), ("⭐", "4,9 en Google"), ("👥", "+1.760 opiniones")]
    fnt_tr = font(FONT_REG, 10)
    col_w = (W - 32) // 3
    for i, (ico, lbl) in enumerate(trust_items):
        cx = 16 + i * col_w + col_w // 2
        ico_w = draw.textbbox((0,0), ico, font=font(FONT_BOLD, 16))[2]
        draw.text((cx - ico_w//2, t_y), ico, font=font(FONT_BOLD, 16), fill=NARANJA)
        lbl_w = draw.textbbox((0,0), lbl, font=fnt_tr)[2]
        draw.text((cx - lbl_w//2, t_y+24), lbl, font=fnt_tr, fill=GRIS_TEXT)

    out = OUT_DIR / f"hero-{v['slug']}-mobile.png"
    canvas.save(out, "PNG", optimize=True)
    return out



if __name__ == "__main__":
    for v in VARIANTES:
        d = make_desktop(v)
        m = make_mobile(v)
        slug = v["slug"]
        print("OK " + slug)
    print("Listo.")
