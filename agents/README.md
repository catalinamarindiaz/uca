# Agentes de IA — Growth Unidad Créditos

Estos son los **primeros agentes** de growth. Cada uno es una "ficha de trabajo" que el asistente (Cursor) puede ejecutar: define **objetivo, fuentes, pasos y formato de salida**. No requieren infraestructura externa para arrancar; se apoyan en las herramientas ya disponibles (web, scripts, MCP).

## Catálogo

| # | Agente | Qué hace | Cadencia | Estado |
|---|---|---|---|---|
| 01 | **Research de Tendencias** | Detecta temas calientes (Trends + prensa) y propone contenido reactivo | Semanal (lun) | ✅ listo |
| 02 | **SEO / Contenidos** | Convierte clusters de keywords en briefs y borradores optimizados | Continuo | ✅ listo |
| 03 | **Vigilancia de Competencia** | Monitorea tasas, promos, SEO y reputación de competidores | Quincenal | ✅ listo |
| 04 | **Social / Community** | Reseñas, prueba social y contenido social | Semanal | 🟡 base |

## Cómo ejecutar un agente
1. Abre la ficha (ej. `agents/01-research-tendencias.md`).
2. Pídele al asistente: *"Ejecuta el agente de Research de Tendencias de esta semana"*.
3. El asistente sigue los pasos, usa las fuentes (`fuentes.yaml`) y entrega la salida en el formato definido.
4. Guarda los entregables en `knowledge-base/outputs/` (créala cuando haya el primer output).

## Principios comunes (aplican a todos)
- **Idioma**: español de Chile.
- **Veracidad**: citar fuente y fecha. No inventar cifras de tasas/condiciones; marcarlas como "verificar".
- **Marca**: respetar tono UNIDAD (cercano, claro, seguro). Reforzar "UNIDAD® nunca pide transferencias".
- **Cumplimiento**: contenido financiero responsable; sin promesas de aprobación garantizada; mencionar "sujeto a evaluación".
- **Anti-fraude**: nunca confundir con `creditosunidad.com` (alerta CMF).

## Próximos agentes (backlog)
- **Lead Ops**: leer envíos de WPForms (MCP) y clasificar leads.
- **Analítica/Conversión**: leer GTM/GA4 y reportar embudo (requiere auth).
- **Calendario editorial** en ClickUp (requiere auth).
