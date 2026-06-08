# Conector: Google Trends

Dos formas de conectar Google Trends, en orden de preferencia.

## Opción A (recomendada) — MCP trendsmcp.ai

Servidor MCP gestionado para datos de tendencias en vivo (Google Search, YouTube, TikTok, Reddit, etc.). Reemplaza a `pytrends` (archivado, con bloqueos 429). Da volumen absoluto y JSON estructurado que el agente razona directo.

- Endpoint: `https://api.trendsmcp.ai/mcp`
- Auth: API key — registro en https://trendsmcp.ai (free tier ~100 req/mes).
- Herramientas:
  - `get_trends(keyword, source='google search', data_mode='weekly'|'daily', period='5y'|'1y'|'3m'|'1m'|'30d')`
  - `get_growth(keyword, ...)` → crecimiento % por período
  - `get_top_trends(source)` → qué es tendencia ahora
  - `get_ranked_trends(source)` → top topics por volumen

### Cómo añadirlo en Cursor
Agregar a la config de MCP de Cursor (ver `.cursor/mcp.example.json` en la raíz del repo). Tras añadirlo y poner la API key, reiniciar/recargar MCP en Cursor.

### Keywords prioritarias para Unidad (monitoreo)
- `crédito automotriz`
- `crédito automotriz entre particulares`
- `crédito sin acreditar ingresos`
- `comprar auto usado`
- `precio bencina` (proxy de sensibilidad al costo de uso)
- nombres de modelos usados populares (Tucson, Suzuki, etc.)

### Uso típico (agente de tendencias / SEO)
1. `get_growth` de las keywords prioritarias → detectar cuáles suben.
2. `get_top_trends('google search')` para CL → temas calientes del momento.
3. Cruzar con clusters SEO (`../02-estrategia/seo-keywords-clusters.md`) y proponer contenido.
4. Guardar el output en `../01-inteligencia-mercado/outputs/`.

## Opción B (fallback, sin dependencias ni API key) — script RSS

`scripts/trends_cl.py` lee el feed RSS oficial de tendencias diarias de Chile
(`https://trends.google.com/trending/rss?geo=CL`) y resalta términos relevantes
(autos, crédito, bencina, normativa).

```
python 04-conectores/scripts/trends_cl.py --solo-relevante
python 04-conectores/scripts/trends_cl.py --json salida.json
```

Limitación: da el *trending diario*, no la curva de interés por keyword (para eso, usar Opción A).

## Cuándo usar cada una
- **Investigación de demanda / estacionalidad de un keyword** → Opción A (MCP).
- **Pulso diario rápido / sin API key / offline-friendly** → Opción B (script).
