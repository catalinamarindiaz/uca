# Agente 05 — Lead Ops & Conversión

> Estado: base inicial. Se activa al autenticar GTM y/o usar WPForms (MCP).

## Objetivo
Conectar la generación de demanda con resultados medibles: **medir, clasificar y optimizar la captación de leads** (simulaciones, WhatsApp, formularios) según el `lead-capture-playbook`.

## Cadencia
Semanal (reporte) + setup inicial de tracking.

## Conectores / inputs (ver `../04-conectores/mcp-registry.yaml`)
- **GTM (MCP)** 🔑 — eventos de conversión: `ver_simulador`, `simulacion_completada`, `click_whatsapp`, `envio_formulario_contacto`, `lead_magnet_descargado`.
- **WPForms (MCP skalling)** — `wpforms/search-entries`, `get-entry` para leer envíos de formularios (cuando aplique al sitio gestionado).
- **Estrategia**: `../02-estrategia/lead-capture-playbook.md`.

## Pasos
1. **Setup** (una vez): definir/verificar que los 5 eventos de conversión existen en GTM.
2. **Lectura**: extraer volumen de eventos y entries por período y fuente.
3. **Clasificación**: marcar leads por calidad (completó simulación, dejó contacto, segmento/persona).
4. **Embudo**: calcular tasas (visita→simulación→contacto→evaluación) y detectar fugas.
5. **Recomendación**: 1–3 acciones de CRO o contenido para mejorar la tasa.

## Formato de salida
`../01-inteligencia-mercado/outputs/leads-YYYY-MM-DD.md`:
```
# Reporte de leads DD-MM-YYYY
## Volumen por evento y fuente
## Embudo y tasas de conversión
## Leads por segmento/persona
## Fugas detectadas
## Acciones recomendadas (CRO / contenido)
```

## Reglas
- No exponer datos personales sensibles; trabajar con agregados/identificadores.
- Cumplimiento de tratamiento de datos.
- Cada hallazgo → una acción accionable.
