# 04 — Conectores (capa de datos vivos)

Esta carpeta es el **puente entre la base de conocimiento y los datos en tiempo real**. Define de dónde sacan información los agentes y cómo se conectan (MCP o scripts), para que la KB no quede estática.

## Cómo funciona

```
Fuente en vivo  ──▶  Conector            ──▶  Agente            ──▶  KB / outputs
(Google Trends,      (MCP o script)           (lee y razona)         (markdown versionado)
 prensa, etc.)
```

- **Scripts propios** (preferido para tendencias): `scripts/tendencias.py` agrega Google News, Wikipedia y Google Trends gratis, sin API keys.
- **MCP**: herramientas que el asistente llama en vivo (GTM, ClickUp, WordPress; Trends de pago opcional).
- Los **agentes** (`../05-agentes/`) consumen estos conectores y guardan resultados en `../01-inteligencia-mercado/outputs/`.

## Archivos
- `scripts/tendencias.py` — **agregador propio de tendencias** (Google News + Wikipedia + Google Trends), gratis y sin API keys.
- `scripts/trends_cl.py` — extractor ligero del trending diario de Chile (fallback).
- `google-trends.md` — guía de las 3 opciones de tendencias (script propio / fallback / MCP de pago).
- `mcp-registry.yaml` — inventario de servidores MCP, estado y para qué se usan.
- `clickup.md` — conectar OAuth, mapeo de listas y flujo agente → tarea.
- `clickup-config.example.yaml` — plantilla de Space/Folder/List (copiar a `clickup-config.yaml`).
- `fuentes.yaml` — fuentes de datos (prensa, competidores, regulación) y su estado.

## Estado actual de los conectores

| Conector | Tipo | Estado | Para qué |
|---|---|---|---|
| Tendencias multi-fuente (propio) | script | ✅ listo | News + Wikipedia + Trends, gratis |
| Google News (es-CL) | script | ✅ listo | momentum de noticias por keyword |
| Wikipedia Pageviews | script | ✅ listo | interés por tema/modelo |
| Google Trends (RSS diario) | script | ✅ listo | trending del día CL |
| Prensa automotriz (La Tercera/Autocosmos/Emol) | script `prensa` | ✅ listo | titulares automotrices recientes |
| Google Trends (trendsmcp.ai) | MCP | 💲 opcional pago | cross-plataforma normalizado |
| Autofact | web | ✅ listo | tasación, trámites, usados |
| GTM | MCP | 🔑 autenticar | tracking de conversión/leads |
| ClickUp | MCP | 🔑 autenticar | tareas y calendario editorial |
| WordPress skalling | MCP | ✅ activo | publicar/SEO en sitio agencia |

## Prioridad de captación de leads
Los conectores existen para alimentar la **estrategia de captación de leads** (`../02-estrategia/lead-capture-playbook.md`): detectar demanda (Trends), crear contenido que la capture (SEO), y medir/optimizar la conversión (GTM).
