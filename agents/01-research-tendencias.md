# Agente 01 — Research de Tendencias

## Objetivo
Detectar semanalmente temas y búsquedas en alza en Chile relevantes para autos, crédito y compra de vehículos, y traducirlos en **oportunidades de contenido reactivo** para UNIDAD.

## Cadencia
Semanal (lunes por la mañana) + alertas ad-hoc ante hechos relevantes (alza de bencina, cambio normativo).

## Fuentes (ver `fuentes.yaml`)
- Google Trends Chile (RSS) → `python scripts/trends_cl.py`
- Emol Autos, La Tercera (motores), BioBioChile (servicios)
- Blog Autofact
- Contexto interno: `knowledge-base/03-buyer-personas.md` (momentos de demanda), `07-seo-keywords-clusters.md`

## Pasos
1. Ejecutar `scripts/trends_cl.py` y revisar el RSS de Trends; extraer términos relacionados con: auto, bencina/combustible, crédito, transporte, normativa vehicular, permiso de circulación, restricción.
2. Escanear las secciones de autos/servicios de la prensa nacional buscando hechos noticiosos accionables.
3. Cruzar con buyer personas y clusters: ¿qué tema conecta con un producto/keyword de UNIDAD?
4. Priorizar 3–5 oportunidades por: relevancia, volumen/tendencia, facilidad de conexión con producto.

## Formato de salida
Archivo `knowledge-base/outputs/tendencias-YYYY-MM-DD.md`:

```
# Tendencias semana DD-MM-YYYY

## Top oportunidades
1. [Tema] — por qué importa | fuente | ángulo para UNIDAD | keyword | CTA a producto
...

## Radar (no priorizado)
- ...

## Acción recomendada
- Brief para agente 02 (SEO/Contenidos): [tema] → cluster X
```

## Criterio de calidad
- Cada oportunidad cita fuente + fecha y propone un **ángulo concreto** (no genérico).
- Conecta explícitamente con un producto (Clásico/Instantáneo/Inteligente) o cluster SEO.
- Distingue temas de **conversión** vs **awareness**.
