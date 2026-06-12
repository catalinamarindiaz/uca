# Auditoría — Propuesta de home con contenido real (10-jun-2026)

**Entregable:** `assets/mockups/home-unidad-contenido-real.html`
**Insumos:** `generar_hero.py` (variante A social proof, corregida y re-ejecutada), fetch de unidadcreditos.cl (10-jun-2026), KB `00-contexto/` y reglas de negocio.

## Verificación claim por claim

| Claim en la propuesta | Fuente | Estado |
|---|---|---|
| 4,9★ con +1.760 opiniones en Google | Sitio (sección reseñas) + empresa.md | ✅ Verificado · ⚠️ el sitio también muestra 4,8★/+160 en otra sección — **pendiente: unificar cifra oficial con el cliente** |
| Gift Card hasta $200.000 o 15% dcto. en tasa (entre particulares) | Sitio (hero promo) + empresa.md | ✅ Verificado |
| Financia hasta 80% del valor del auto | Sitio + empresa.md | ✅ Verificado |
| Clásico: pie mín. 20%, 6–60 meses, 1ª cuota 60 días, uso particular/comercial | Sitio + productos.md | ✅ Verificado |
| Instantáneo: sin acreditar ingresos, pie >35%, cuota fija en $, 1ª cuota 60 días | Sitio + productos.md | ✅ Verificado |
| Inteligente: renueva cada 2/3 años, pie mín. 20%, nuevos y seminuevos | Sitio + productos.md | ✅ Verificado |
| Validación oficial · transferencia y financiamiento en 1 día · pie directo al vendedor | Sitio (sección particulares) + empresa.md | ✅ Verificado |
| +500 concesionarias (Santiago, Concepción, Viña, La Serena) | Sitio + empresa.md | ✅ Verificado |
| Ejecutivas: Elizabeth Estrada, Gilda Maureira, Camila Pérez, Zahara Santamaria, Yvi Silva (fotos CDN) | Sitio (home) | ✅ Verificado |
| 3 reseñas (Juan Fernández, Viviana Avendaño, Laura Muñoz V.) con links share.google | Sitio (home, 9-jun-2026) | ✅ Verificado |
| Automotoras Silco, Auto Justo, JVP, Príncipe de Gales | Sitio (alianzas en home) | ✅ Verificado |
| Dirección, teléfono, links nav/footer, portal pago bora.cl, solicitud.unidadcreditos.cl | Sitio | ✅ Verificado |

## Correcciones por reglas de negocio (AGENTS.md + memoria del proyecto)

| Texto original (script/mockup) | Acción | Regla |
|---|---|---|
| "+1.750 créditos aprobados" | Corregido a "+1.760 opiniones en Google" | No inventar cifras (eran opiniones, no créditos) |
| "+20.000 créditos / clientes" | **Eliminado** | Cifra no verificada en KB ni sitio |
| "Empresa regulada" | **Eliminado** | Registro CMF es pregunta abierta en empresa.md |
| "Tasas de interés competitivas" (paso 2 del sitio) | Reemplazado por "evaluación rápida y transparente + acompañamiento" | Diferenciador real = acompañamiento, no tasa |
| Promo "$50.000" del mockup original | Reemplazado por Gift Card $200.000 / 15% dcto. real | Contenido real del sitio |

## Cumplimiento

- "Crédito sujeto a evaluación" en hero y CTA final (nunca prometer aprobación).
- Antifraude en 3 puntos: topbar, sección dedicada y footer ("nunca pide transferencias", pie directo al vendedor, dominio oficial unidadcreditos.cl).
- Sin contenido dirigido a segmentos no habilitados (Dicom, conductores de apps).
- Sin "estafa/fraude" en títulos (se usa "compra segura", "hazlo seguro").
- Énfasis en acompañamiento + entre particulares (diferenciador real).

## v2 — Home conversion-first (`home-unidad-conversion-particulares.html`)

Rediseño tras feedback: la v1 era una réplica auditada del sitio, no una página de conversión.
La v2 se diseña desde `lead-capture-playbook.md` + Persona A:

- **H1 = momento del usuario** ("¿Encontraste el auto en Marketplace o a un particular?"), no branding. Mensaje ganador de Persona A: validamos al vendedor, pie directo a él, transferencia en 1 día.
- **Formulario multipaso embebido en el hero** (paso 1 de un tap, pre-calificación por pie ≥20%/35%, captura de WhatsApp antes del handoff a solicitud.unidadcreditos.cl). Captura el lead aunque no termine el flujo oficial.
- **Promo Gift Card pegada al formulario** (incentivo en el punto de decisión, no en sección aparte).
- **Una sola meta de conversión**: nav reducida, sin promos ni secciones que compitan; productos Instantáneo/Inteligente quedan como salida secundaria al final (Personas B y C).
- **Prueba social y antifraude junto a cada CTA** (reductores de fricción según playbook).
- **Sticky CTA móvil** (simular + WhatsApp), mobile-first.
- **Eventos GTM del playbook instrumentados**: `ver_simulador`, `simulacion_completada`, `click_whatsapp` vía dataLayer.
- Cumplimiento verificado por script: sin cuotas/tasas calculadas, "sujeto a evaluación" x6, sin Dicom/app-drivers, sin "estafa" en títulos.
- **Pendiente de implementación**: traspaso de datos del lead al funnel oficial (parámetros o API con el equipo de solicitud).

## Cambios al script `generar_hero.py`

1. Rutas relativas al repo (antes apuntaban a una sesión específica y fallaban).
2. Salida a `assets/mockups/` (versionable).
3. Claims corregidos en las 3 variantes (ver tabla anterior).
