# Reporte de Revisión Técnica — Artículos junio 2026
Fecha: 15 junio 2026
Revisor: Agente 06 (revisión técnica)
Artículos revisados: 4

---

## 1. contenido-chevrolet-sail-usado-chile.md

### Errores críticos (bloquean publicación)

| # | Ubicación | Texto original | Error | Corrección | Fuente |
|---|---|---|---|---|---|
| 1 | Sección "¿Cómo financiar?" | "A 48 meses, la cuota de referencia es aproximadamente $245.000–$265.000 mensuales" | **Cuota inventada** — viola regla de negocio UNIDAD | Eliminar párrafo de cuotas. Reemplazar con: "La cuota depende de la tasa aprobada según tu perfil — habla con una ejecutiva UNIDAD para conocer las condiciones exactas." + CTA | Regla interna: feedback_no_inventar_cuotas.md |
| 2 | Sección "¿Cómo financiar?" | "a 36 meses la cuota sube a aproximadamente $300.000–$320.000" | **Cuota inventada** — misma violación | Mismo tratamiento que error #1 | Regla interna |
| 3 | FAQ "¿Cuánto gasta de bencina el Chevrolet Sail?" | "consumo promedio de **14 a 16 km por litro** en ciudad" | **Incorrecto**: 14-16 km/l es el consumo MIXTO/ruta, no ciudad. Consumo ciudad oficial: ~10.6 km/l (Sail 1.5 LTZ CVT 2025) | Corregir a: "rendimiento mixto de 14–16 km/litro. En ciudad, el consumo real ronda los 10–11 km/litro" | Autocosmos.cl — ficha Sail 1.5 LTZ Aut 2025: Ciudad 10.6, Ruta 18.9, Mixto 14.7 km/l |
| 4 | CTA al pie del artículo | "ingresa el valor del Sail que encontraste y elige el plazo que más te acomoda" | **Simulador automático no existe** en UNIDAD. Implica herramienta self-service. | CTA correcto: "Habla con una ejecutiva UNIDAD para simular tu crédito" | Regla interna: feedback_no_inventar_cuotas.md |

### Errores menores

| # | Ubicación | Texto original | Corrección | Fuente |
|---|---|---|---|---|
| 5 | Tabla versiones Sail | Motor "1.4 manual" para 2012–2017 | Confirmar: Sail 2012 sí era 1.4L (1399cc, 102HP) — dato **correcto**, pero agregar la potencia para precisión | Autocosmos.cl — Chevrolet Sail 1.4 LT (2012) |
| 6 | Tabla — Sail 2024 "LTZ CVT" | Cita versión LTZ para 2024 | LTZ aparece documentada en **2025** (LTZ R, LTZ S, LTZ Aut). Verificar si existía en 2024 o el año de entrada al mercado chileno. Citar como "LTZ (disponible desde 2025)" o ajustar año. | Autocosmos.cl — Sail 2025: LTZ R $10.690.000, LTZ S $11.190.000, LTZ Aut $11.690.000 |
| 7 | Sección "Qué revisar — Revisión técnica" | "revisión técnica vigente" (sin especificar frecuencia) | Agregar nota: "Para autos particulares la revisión técnica es **anual**. Solo los autos 0 km tienen 2 años de gracia antes de la primera." | Autofact.cl — Calendario revisión técnica |

### Estado: ❌ NO APROBADO — requiere corrección de errores 1–4 antes de publicar

---

## 2. credito-automotriz-entre-particulares.md

### Errores críticos

| # | Ubicación | Texto original | Error | Corrección | Fuente |
|---|---|---|---|---|---|
| 1 | Paso 1 del proceso | "un **Ejecutivo Financiero** de UNIDAD® te entrega las condiciones" | Masculino incorrecto — UNIDAD usa "ejecutivas" (femenino) en toda su comunicación | Cambiar a "una **ejecutiva** de UNIDAD® te entrega las condiciones" | Regla de negocio: `00-contexto/empresa.md` + comunicación oficial UNIDAD |
| 2 | CTA al cierre | "[Simular mi crédito]" con texto implícito de self-service | Simulador automático no existe | CTA: "[Hablar con una ejecutiva UNIDAD]" → `/simula-credito-automotriz` | Regla interna |

### Errores menores

Ninguno adicional. El resto del artículo (condiciones, proceso, FAQ, anti-fraude) está correcto y alineado con la KB de productos.

### Estado: ⚠️ APROBADO CON CORRECCIONES — 2 cambios puntuales

---

## 3. contenido-simulador-credito-automotriz.md

### Error estructural (requiere decisión editorial)

| # | Tipo | Descripción |
|---|---|---|
| 1 | **Premisa incorrecta** | El artículo entero explica cómo usar un "simulador de crédito automotriz" automático (ingresar datos → cuota en segundos). UNIDAD **no tiene simulador automático**. El proceso es con una ejecutiva real. |
| 2 | Texto específico | "En segundos tienes una cuota de referencia y puedes continuar con una ejecutiva real" — falso: no hay simulador que entregue cuotas en segundos. |
| 3 | Texto específico | "ingresa el valor del auto, el pie que puedes pagar y el plazo que buscas. En segundos tienes una cuota de referencia" — misma violación. |
| 4 | Sección CAE | Sección técnicamente correcta (CAE, cómo leer resultados) pero construida sobre la premisa de que existe una herramienta que calcula automáticamente. |

### Recomendación

**Opción A (reescritura):** Transformar el artículo en "Qué variables afectan tu cuota de crédito automotriz" — artículo educativo que explica los mismos conceptos (pie, plazo, tasa, CAE) sin implicar que hay un simulador automático. CTA: "Habla con una ejecutiva para que calcule tu cuota según tu perfil."

**Opción B (eliminación):** Eliminar el artículo si el URL `/simula-credito-automotriz` ya existe como landing funcional. El artículo satélite podría generar confusión o canibalización.

### Estado: ❌ NO APROBADO — requiere decisión editorial antes de cualquier acción

---

## 4. credito-automotriz-sin-acreditar-ingresos.md

### Errores menores

| # | Ubicación | Texto original | Corrección | Fuente |
|---|---|---|---|---|
| 1 | Paso 1 del proceso | "**Simula tu crédito** en unidadcreditos.cl" | El simulador no es automático. Ajustar a: "**Contacta a una ejecutiva** en unidadcreditos.cl para revisar tu caso" | Regla interna |
| 2 | Cierre del artículo | "**simula tu crédito automotriz** y pregunta por el Crédito Instantáneo" | Mismo ajuste de CTA | Regla interna |

### Advertencias

- El artículo menciona que el Instantáneo puede usarse "entre particulares, según tu caso" — ✅ correcto y bien caveateado.
- Los requisitos (cédula, domicilio, sin liquidaciones) están alineados con la KB de productos.
- La tabla de condiciones está correctamente marcada como "referencial y sujeta a evaluación".

### Estado: ⚠️ APROBADO CON CORRECCIONES — 2 cambios de CTA

---

## Resumen ejecutivo

| Artículo | Estado | Acción requerida |
|---|---|---|
| chevrolet-sail-usado-chile.md | ❌ NO APROBADO | Eliminar cuotas inventadas + corregir consumo + ajustar CTA + verificar año LTZ |
| credito-automotriz-entre-particulares.md | ⚠️ CON CORRECCIONES | 2 cambios puntuales (género ejecutiva, CTA) |
| contenido-simulador-credito-automotriz.md | ❌ NO APROBADO | Decisión editorial: reescribir o eliminar |
| credito-automotriz-sin-acreditar-ingresos.md | ⚠️ CON CORRECCIONES | 2 ajustes de CTA |

## Hechos verificados en esta revisión (para KB)

- **Revisión técnica Chile — autos particulares**: ANUAL. Los autos 0 km tienen 2 años de gracia (Certificado de Homologación) → luego anual. Nunca "cada 2 años" para autos usados. Fuente: [Autofact.cl](https://www.autofact.cl/blog/mi-auto/revision-tecnica/calendario-2019)
- **Chevrolet Sail 2012**: Motor 1.4L (1399cc, 102 HP), manual 5 vel. ✅ Correcto en artículo. Fuente: [Autocosmos.cl](https://www.autocosmos.cl/catalogo/2012/chevrolet/sail/14-lt/150889)
- **Chevrolet Sail consumo**: Ciudad ~10.6 km/l | Ruta ~18.9 km/l | Mixto ~14.7 km/l (Sail 1.5 LTZ Aut 2025). Fuente: [Autocosmos.cl](https://www.autocosmos.cl/catalogo/2025/chevrolet/sail/15-ltz-aut/178879)
- **Chevrolet Sail LTZ**: Existe en Chile como LTZ R, LTZ S y LTZ Aut documentado desde 2025. Verificar si aplica para 2024.
- **Sail 2025 versiones (precios de lista)**: LT $9.990.000 | LTZ R $10.690.000 | LTZ S $11.190.000 | LTZ Aut $11.690.000. Fuente: Autocosmos.cl
