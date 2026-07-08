# Agentes de IA — Growth Unidad Créditos

Estos son los **primeros agentes** de growth. Cada uno es una "ficha de trabajo" que el asistente (Cursor) puede ejecutar: define **objetivo, fuentes, pasos y formato de salida**. No requieren infraestructura externa para arrancar; se apoyan en las herramientas ya disponibles (web, scripts, MCP).

## Catálogo

| # | Agente | Qué hace | Cadencia | Estado |
|---|---|---|---|---|
| 01 | **Research de Tendencias** | Detecta temas calientes (Trends + prensa) y propone contenido reactivo | Semanal (lun) | ✅ listo |
| 02 | **SEO / Contenidos** | Convierte clusters de keywords en briefs y borradores optimizados | Continuo | ✅ listo |
| 03 | **Vigilancia de Competencia** | Monitorea tasas, promos, SEO y reputación de competidores | Quincenal | ✅ listo |
| 04 | **Social / Community** | Reseñas, prueba social y contenido social | Semanal | 🟡 base |
| 05 | **Lead Ops & Conversión** | Mide, clasifica y optimiza la captación de leads (GTM/WPForms) | Semanal | 🟡 base |

## Cómo ejecutar un agente
1. Abre la ficha (ej. `05-agentes/01-research-tendencias.md`).
2. Pídele al asistente: *"Ejecuta el agente de Research de Tendencias de esta semana"*.
3. El asistente sigue los pasos, usa las fuentes (`fuentes.yaml`) y entrega la salida en el formato definido.
4. Guarda los entregables en `01-inteligencia-mercado/outputs/`. Los conectores de datos (incl. Google Trends) están en `04-conectores/`.

## Principios comunes (aplican a todos)
- **Idioma**: español de Chile.
- **Veracidad**: citar fuente y fecha. No inventar cifras de tasas/condiciones; marcarlas como "verificar".
- **Marca**: respetar tono UNIDAD (cercano, claro, seguro). Reforzar "UNIDAD® nunca pide transferencias".
- **Cumplimiento**: contenido financiero responsable; sin promesas de aprobación garantizada; mencionar "sujeto a evaluación".
- **Anti-fraude**: nunca confundir con `creditosunidad.com` (alerta CMF).

## Próximos agentes (backlog)
- **Calendario editorial** en ClickUp (requiere auth).
- **Ads / Performance**: lectura de campañas y costo por lead (si se activan Ads).
- **Reputación**: gestión de reseñas vía Google Business Profile (requiere acceso).
