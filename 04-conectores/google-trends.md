# Conector: Tendencias (multi-fuente, propio y gratis)

Tres formas de obtener tendencias, en orden de preferencia. La **Opción A es propia y gratis** (recomendada); la B es un fallback simple; la C es un servicio de pago opcional.

## Opción A (recomendada) — Script propio multi-fuente · `scripts/tendencias.py`

Agregador propio que consulta **directo el origen** de cada señal, **sin API keys ni costo**, usando solo la biblioteca estándar de Python. Hecho a medida para Unidad Créditos (keywords de auto/crédito + contexto Chile).

### Fuentes (gratis) que cubre
| Conector | Origen | Qué entrega |
|---|---|---|
| `daily` | Google Trends RSS (geo=CL) | términos más buscados del día en Chile |
| `news` | Google News RSS (es-CL) | **volumen de noticias por keyword** (momentum) + titulares |
| `prensa` | RSS prensa automotriz (La Tercera MTOnline, Autocosmos) + Emol vía Google News | titulares automotrices recientes por medio |
| `wikipedia` | Wikipedia Pageviews REST API | vistas e interés por tema/modelo + Δ 7d vs 7d |
| `pytrends` (opcional) | Google Trends no oficial | interés en el tiempo por keyword (requiere `pip install pytrends`) |

> El conector `prensa` intenta el RSS nativo de la sección de autos de cada medio y, si falla, cae a Google News acotado a la sección del medio (evita noticias policiales/generales).

### Uso
```bash
# Informe completo (daily + news + wikipedia)
python 04-conectores/scripts/tendencias.py

# Solo noticias, ventana de 14 días, guardando salidas
python 04-conectores/scripts/tendencias.py --fuentes news --dias 14 \
  --md 01-inteligencia-mercado/outputs/tendencias-$(date +%F).md \
  --json 01-inteligencia-mercado/outputs/tendencias-$(date +%F).json

# Keywords / artículos personalizados
python 04-conectores/scripts/tendencias.py \
  --keywords "crédito automotriz" "comprar auto usado" \
  --wiki "Hyundai_Tucson" "Tesla,_Inc."

# Incluir pytrends (interés en el tiempo)
python 04-conectores/scripts/tendencias.py --pytrends
```

### Notas
- Cada conector **falla de forma aislada**: si una fuente cae, las demás siguen.
- `news` es el mejor proxy de demanda/actualidad para este negocio (ej. picos de "restricción vehicular", "precio bencina").
- `wikipedia` usa ventana mínima de 30 días para calcular el momentum (Δ 7d).
- Salida en consola (UTF-8), y opcionalmente `--md` / `--json` a `01-inteligencia-mercado/outputs/`.

### Cómo extenderlo (añadir fuentes)
Agregar una función conector que devuelva un dict y enchufarla en `correr()` + `a_markdown()`. Candidatos gratis a futuro: Reddit (.json público), YouTube (requiere API key), RSS de prensa automotriz (Emol/Latercera), Banco Central / SII para señales económicas.

## Opción B (fallback simple) — `scripts/trends_cl.py`
Versión ligera que solo lee el trending diario de Chile (Google Trends RSS). Útil para un pulso rápido. La Opción A ya incluye esto en su conector `daily`.

```bash
python 04-conectores/scripts/trends_cl.py --solo-relevante
```

## Opción C (opcional, de pago) — MCP trendsmcp.ai
Servicio gestionado con ~25+ fuentes normalizadas a índice 0–100 (Google, YouTube, TikTok, Reddit, Amazon, etc.). Free tier de **100 req/mes**; más allá, es **de pago**.
- Endpoint: `https://api.trendsmcp.ai/mcp` · Auth: API key (`.cursor/mcp.example.json`).
- Conviene solo si necesitamos **comparación cross-plataforma normalizada** o volumen absoluto que no obtenemos gratis. Para el día a día de Unidad, la Opción A es suficiente.

## Cuándo usar cada una
- **Operación diaria / informes semanales** → Opción A (propia, gratis).
- **Pulso rápido del trending del día** → Opción B.
- **Benchmark cross-plataforma normalizado puntual** → Opción C (evaluar costo).
