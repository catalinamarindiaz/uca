# 04 — Conectores (capa de datos vivos)

Esta carpeta es el **puente entre la base de conocimiento y los datos en tiempo real**. Define de dónde sacan información los agentes y cómo se conectan (MCP o scripts), para que la KB no quede estática.

## Cómo funciona

```
Fuente en vivo  ──▶  Conector            ──▶  Agente            ──▶  KB / outputs
(Google Trends,      (MCP o script)           (lee y razona)         (markdown versionado)
 prensa, etc.)
```

- **MCP** (preferido): herramientas que el asistente llama en vivo (Trends, GTM, ClickUp, WordPress).
- **Scripts** (fallback sin dependencias): p. ej. `scripts/trends_cl.py` para Google Trends vía RSS.
- Los **agentes** (`../05-agentes/`) consumen estos conectores y guardan resultados en `../01-inteligencia-mercado/outputs/`.

## Archivos
- `mcp-registry.yaml` — inventario de servidores MCP, estado y para qué se usan.
- `google-trends.md` — cómo conectar Google Trends por MCP (recomendado) y por script (fallback).
- `fuentes.yaml` — fuentes de datos (prensa, competidores, regulación) y su estado.
- `scripts/trends_cl.py` — extractor de tendencias diarias de Chile (sin dependencias).

## Estado actual de los conectores

| Conector | Tipo | Estado | Para qué |
|---|---|---|---|
| Google Trends (trendsmcp.ai) | MCP | ⛏️ por añadir | volumen/keywords/breakouts en vivo |
| Google Trends (RSS) | script | ✅ listo | tendencias diarias CL (fallback) |
| Prensa automotriz | web | ✅ listo | noticias/ángulos de contenido |
| Autofact | web | ✅ listo | tasación, trámites, usados |
| GTM | MCP | 🔑 autenticar | tracking de conversión/leads |
| ClickUp | MCP | 🔑 autenticar | tareas y calendario editorial |
| WordPress skalling | MCP | ✅ activo | publicar/SEO en sitio agencia |

## Prioridad de captación de leads
Los conectores existen para alimentar la **estrategia de captación de leads** (`../02-estrategia/lead-capture-playbook.md`): detectar demanda (Trends), crear contenido que la capture (SEO), y medir/optimizar la conversión (GTM).
