# AGENTS.md — Contexto del proyecto para asistentes de IA

> Este archivo es la **fuente de contexto canónica** para cualquier asistente de IA que trabaje en el repo (Cursor, Claude Code, etc.). Léelo antes de actuar. La regla de Cursor (`.cursor/rules/contexto-unidad-creditos.mdc`) apunta aquí.

## El proyecto
Growth digital y generación de contenido para **UNIDAD® Crédito Automotriz** ([unidadcreditos.cl](https://www.unidadcreditos.cl/)), **cliente de Skalling — Aceleración Digital** ([skalling.com](https://www.skalling.com)).
Repo oficial (privado): `agilerod/unidad_creditos_contenido`. No mezclar con otros proyectos.

## Qué es UNIDAD (resumen)
Financiera chilena de **crédito automotriz**, diferenciada en **crédito entre particulares** (financiar la compra de un auto usado a otra persona). Proceso 100% digital con ejecutivas reales. Productos: **Clásico** (pie 20%, 6–60m), **Instantáneo** (no acredita ingresos, pie >35%), **Inteligente** (renovar auto cada 2–3 años). Detalle en `00-contexto/`.

## Reglas (obligatorias)
- **Idioma**: español de Chile.
- **No inventar cifras** de tasas, pie, plazos o ratings. Si no están verificadas en la KB, marcar "verificar".
- **Cumplimiento financiero**: nunca prometer aprobación; usar "sujeto a evaluación".
- **Anti-fraude**: el sitio oficial es **unidadcreditos.cl** y "UNIDAD® nunca pide transferencias de dinero". Hay alerta CMF por `creditosunidad.com` (NO es UNIDAD); jamás confundirlos.
- **Diferenciador a defender**: entre particulares + pie bajo (20%) + plazo largo (60m) + sin acreditar ingresos + transferencia en 1 día + seguridad.

## Estructura del repo
| Carpeta | Contenido |
|---|---|
| `00-contexto/` | empresa, productos, buyer-personas |
| `01-inteligencia-mercado/` | competencia, fuentes-de-datos, `outputs/` (entregables de agentes) |
| `02-estrategia/` | growth-strategy, seo-keywords-clusters, lead-capture-playbook |
| `03-contenido/` | `briefs/` y `articulos/` (entregables de contenido) |
| `04-conectores/` | datos vivos: `mcp-registry.yaml`, `google-trends.md`, `fuentes.yaml`, `scripts/` |
| `05-agentes/` | fichas de los agentes de growth (cómo ejecutarlos) |
| `.cursor/` | regla de contexto + `mcp.example.json` |

## Herramientas de datos
- **Tendencias (propio, gratis)**: `python 04-conectores/scripts/tendencias.py` (Google News + prensa automotriz + Wikipedia + Trends RSS; `pytrends` opcional). Ver `04-conectores/google-trends.md`.
- **MCP**: `skalling-wordpress` (activo), `gtm` y `clickup` (requieren autenticar). Inventario y estado en `04-conectores/mcp-registry.yaml`.

## Flujo de contenido
1. Detectar demanda → `tendencias.py` + agente 01 (output a `01-inteligencia-mercado/outputs/`).
2. Brief SEO → `03-contenido/briefs/` (agente 02, backlog desde `02-estrategia/seo-keywords-clusters.md`).
3. Artículo → `03-contenido/articulos/` con front-matter (title/meta/slug) y CTA medible.
4. Captación/medición → `02-estrategia/lead-capture-playbook.md` + GTM (agente 05).

## Convenciones de trabajo (colaboración)
- **Commits**: estilo Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`...), mensaje en español.
- **Ramas**: `main` estable; trabajar en ramas `feat/...`, `fix/...`, `content/...` y abrir Pull Request.
- **No** commitear secretos (API keys, tokens). Usar `.cursor/mcp.example.json` con placeholders.
- Entregables generados van en `01-inteligencia-mercado/outputs/` (los `.json` están en `.gitignore`).
- Ver `CONTRIBUTING.md` para el detalle del flujo de GitHub.

## Para Claude / otros asistentes
Este repo no requiere build. Python 3.8+ con biblioteca estándar para los scripts (sin dependencias salvo `pytrends` opcional, en `requirements.txt`). Respeta las reglas de arriba y la estructura de carpetas al crear archivos.
