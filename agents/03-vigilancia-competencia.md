# Agente 03 — Vigilancia de Competencia

## Objetivo
Mantener actualizado el panorama competitivo: **condiciones (pie, plazo, tasa), promociones, contenido/SEO y reputación** de los competidores, y alertar cambios relevantes.

## Cadencia
Quincenal + alerta ad-hoc ante promociones agresivas.

## Competidores objetivo (ver `fuentes.yaml`)
- Directos "entre particulares": **Tanner ONE**, **Dily**, **Autofin**
- Grandes: **Forum**, **BK**
- Complementario/aliado potencial: **Autofact** (no compite, pero define el ecosistema)

## Qué vigilar (vectores)
1. **Condiciones**: pie mínimo, plazo máximo, monto máximo, requisitos (edad, ingresos), tasas publicadas.
2. **Promociones**: bonos, gift cards, transferencia/inspección gratis, meses de gracia.
3. **Contenido/SEO**: nuevos artículos, keywords que atacan, estructura de blog.
4. **Reputación**: rating Google y nº de reseñas.
5. **Mensajería**: cómo se posicionan (seguridad, rapidez, digital).

## Pasos
1. Revisar la home y páginas de producto/financiamiento de cada competidor.
2. Registrar cambios vs el último snapshot (`knowledge-base/04-analisis-competencia.md` + outputs previos).
3. Detectar amenazas/oportunidades para UNIDAD.
4. Recomendar ajustes de oferta o mensaje.

## Formato de salida
Archivo `knowledge-base/outputs/competencia-YYYY-MM-DD.md`:
```
# Vigilancia competencia DD-MM-YYYY

## Cambios detectados
- [Competidor]: [qué cambió] (antes → ahora) | fuente

## Tabla comparativa actualizada
| Competidor | Pie | Plazo | Monto máx | Promo vigente | Rating |

## Amenazas / Oportunidades
- ...

## Recomendaciones para UNIDAD
- ...
```

## Criterio de calidad
- Datos con fuente y fecha; condiciones marcadas "verificar" si no están explícitas.
- Foco accionable: cada hallazgo → una recomendación.
- Mantener actualizado el benchmark de la KB (`04-analisis-competencia.md`).
