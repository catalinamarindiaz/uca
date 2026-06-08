# 05 — Fuentes de Datos (validación de acceso)

> Validado el 8-jun-2026. Estado: ✅ accesible / ⚠️ con limitación / 🔑 requiere credencial.
> Detalle máquina-legible en `agents/fuentes.yaml`.

## Resumen

| Fuente | Estado | Cómo se accede | Uso |
|---|---|---|---|
| Google Trends (Chile) | ✅ | RSS `trends.google.com/trending/rss?geo=CL` + script | Tendencias de búsqueda diarias |
| Google Trends (interés por keyword) | ⚠️ | Web/JS o lib `pytrends` (no oficial) | Estacionalidad de "crédito automotriz", etc. |
| Emol Autos | ✅ | `emol.com/autos/` (HTML legible) | Noticias y tendencias automotrices |
| La Tercera / MT Online | ✅ | `latercera.com` (sección motores) | Noticias automotrices |
| BioBioChile (autos/servicios) | ✅ | `biobiochile.cl` | Restricción vehicular, normativa, bencina |
| Autofact | ✅ | `autofact.cl` (público) + Blog | Tasación, precios usados, tendencias, trámites |
| Competidores (Forum/Tanner/Autofin/Dily/BK) | ✅ | Webs públicas | Tasas, promos, contenido |
| CMF Chile (alertas de fraude) | ✅ | `cmfchile.cl` | Confianza/regulación, alertas |
| Diario Financiero | ⚠️ | `df.cl` (parcial, muro de pago) | Resultados del sector |
| Google Search Console / Analytics | 🔑 | Requiere acceso del cliente | SEO real, conversiones |
| Google Tag Manager (MCP) | 🔑 | MCP `gtm` (autenticar) | Tracking de eventos/conversión |
| ClickUp (MCP) | 🔑 | MCP `clickup` (autenticar) | Operación: tareas y calendario |
| WordPress skalling.com (MCP) | ✅ | MCP `skalling-wordpress` | Publicación/SEO en sitio agencia |

---

## 1. Google Trends — Chile ✅
**Validado.** El feed RSS de tendencias diarias responde sin autenticación:
```
https://trends.google.com/trending/rss?geo=CL
```
Devuelve los términos más buscados del día con tráfico aproximado y noticias asociadas (ej. del 8-jun: "restricción vehicular hoy", "ipc", "demre"...).

- **Automatización**: `python scripts/trends_cl.py` parsea el RSS (sin dependencias externas) y filtra por palabras clave de interés (auto, crédito, bencina, etc.).
- **Limitación**: el RSS da *trending diario*, no la curva de "interés en el tiempo" de un keyword específico. Para eso:
  - Opción A: `pytrends` (librería no oficial; riesgo de rate-limit / bloqueo).
  - Opción B: exportación manual CSV desde trends.google.com y guardarla en `knowledge-base/data/`.
  - Opción C (recomendada a futuro): Google Trends vía consultas comparativas trimestrales documentadas.

## 2. Prensa automotriz nacional (Chile) ✅
Secciones validadas y accesibles como HTML legible:
- **Emol Autos** — `https://www.emol.com/autos/` (novedades, destacados, mercado).
- **La Tercera (Motores/MT)** — `https://www.latercera.com/` (buscar sección motores).
- **BioBioChile** — `https://www.biobiochile.cl/` (servicios: restricción vehicular, bencina, normativa — muy ligado a la demanda de autos).
- **Cooperativa / T13 / 24horas** — cobertura económica y de servicios útil para contenido de actualidad.

**Uso**: alimentar el blog con contenido de actualidad (precio bencina, restricción, leyes) que ya rankea UNIDAD, y detectar ángulos noticiosos.

## 3. Autofact ✅
`https://www.autofact.cl/` — público. Útil como **fuente de datos y de contenido**, no como competidor (Autofact es informes/transferencia, complementario al crédito):
- Herramientas: tasación / valor comercial de usados, valor permiso de circulación, valor transferencia, revisión técnica.
- **Blog Autofact** y podcast "Detrás del Volante" → cantera de temas y benchmarking de contenido.
- Parte de **CAR Group** (internacional).
- **Sinergia**: UNIDAD valida vehículo/vendedor; Autofact provee historial/tasación → contenido conjunto "cómo comprar usado seguro".

## 4. Competidores ✅
Webs públicas, revisables por el agente de competencia:
- Forum `forum.cl`, Tanner `tanner.cl/automotriz`, Autofin `autofin.cl`, Dily `dily.cl`, BK `bk.cl`.

## 5. CMF Chile (regulación / fraude) ✅
`https://www.cmfchile.cl/` — Sección de **alertas de fraude** (incluye listado de créditos fraudulentos). Relevante: alerta sobre `creditosunidad.com` (NO es UNIDAD). Usar para contenido de confianza y para verificar legitimidad.

---

## Fuentes que requieren credenciales del cliente / autenticación 🔑

### Pendientes de pedir al cliente (UNIDAD)
- Acceso (lectura) a **Google Search Console** y **Google Analytics 4** del dominio unidadcreditos.cl.
- Acceso a **Google Business Profile** (gestión de reseñas).
- Acceso a **Meta Ads / Google Ads** (si hay campañas activas).
- Confirmar **CMS del sitio** (parece Wix) para definir flujo de publicación.

### MCP a autenticar (acción del usuario en Cursor)
- **gtm** (Google Tag Manager): para implementar y leer eventos de conversión (clic en simulador, clic WhatsApp, envío de formulario).
- **clickup**: para llevar el backlog de growth y el calendario editorial.
- **skalling-wordpress**: ✅ ya activo (sitio de la agencia skalling.com; Divi + WPForms + Rank Math).

> Para autenticar GTM/ClickUp: pídeselo al asistente ("autentica el MCP de GTM") o conéctalos desde la configuración de MCP de Cursor.
