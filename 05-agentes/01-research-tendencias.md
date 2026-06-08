# Agente 01 — Research de Tendencias

## Objetivo
Detectar semanalmente temas y búsquedas en alza en Chile relevantes para autos, crédito y compra de vehículos, y traducirlos en **oportunidades de contenido reactivo** para UNIDAD.

## Cadencia
Semanal (lunes por la mañana) + alertas ad-hoc ante hechos relevantes (alza de bencina, cambio normativo).

## Fuentes (ver `fuentes.yaml`)
- Google Trends (MCP trendsmcp.ai) → `get_growth`/`get_top_trends` (ver `../04-conectores/google-trends.md`)
- Google Trends Chile (RSS, fallback) → `python 04-conectores/scripts/trends_cl.py`
- Emol Autos, La Tercera (motores), BioBioChile (servicios)
- Blog Autofact
- Contexto interno: `../00-contexto/buyer-personas.md` (momentos de demanda), `../02-estrategia/seo-keywords-clusters.md`

## Pasos
1. Consultar Google Trends (MCP) para las keywords prioritarias y/o ejecutar `04-conectores/scripts/trends_cl.py`; extraer términos relacionados con: auto, bencina/combustible, crédito, transporte, normativa vehicular, permiso de circulación, restricción.
2. Escanear las secciones de autos/servicios de la prensa nacional buscando hechos noticiosos accionables.
3. Cruzar con buyer personas y clusters: ¿qué tema conecta con un producto/keyword de UNIDAD?
4. Priorizar 3–5 oportunidades por: relevancia, volumen/tendencia, facilidad de conexión con producto.

## Formato de salida
Archivo `../01-inteligencia-mercado/outputs/tendencias-YYYY-MM-DD.md`:

```
# Tendencias semana DD-MM-YYYY

## Top oportunidades
1. [Tema] — por qué importa | fuente | ángulo para UNIDAD | keyword | CTA a producto
...

## Radar (no priorizado)
- ...

## Acción recomendada
- Brief para agente 02 (SEO/Contenidos): [tema] → cluster X
```

## Criterio de calidad
- Cada oportunidad cita fuente + fecha y propone un **ángulo concreto** (no genérico).
- Conecta explícitamente con un producto (Clásico/Instantáneo/Inteligente) o cluster SEO.
- Distingue temas de **conversión** vs **awareness**.
