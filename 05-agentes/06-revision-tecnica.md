# Agente 06 — Revisión Técnica de Contenidos

## Objetivo
Validar cada artículo o pieza de contenido generada por el agente 02 (SEO/Contenidos) **antes de publicar**, contrastando cada dato técnico, normativo o de negocio contra fuentes oficiales. Si encuentra un error, lo documenta con fuente, corrección y nivel de criticidad.

## Cuándo ejecutar
- Antes de aprobar cualquier artículo para publicación.
- Al actualizar artículos existentes (cambios de precio, regulación, producto).
- Cuando el agente 02 produzca datos que no estén en la KB verificada (`00-contexto/`, `knowledge-base/`).

---

## Checklist de revisión (ejecutar en orden)

### 1. Reglas de negocio UNIDAD® (fuente: `AGENTS.md` + `00-contexto/productos.md` + memoria)

| Ítem | Verificar |
|---|---|
| Cuotas estimadas | **Prohibido publicar.** Solo monto financiado + CTA a ejecutiva. |
| Simulador automático | **No existe.** CTA correcto: "Habla con una ejecutiva" → `/simula-credito-automotriz` |
| Conductores de apps (Uber, DiDi, Cabify) | No califican para crédito UNIDAD. No crear contenido para ese perfil. |
| Personas con Dicom | No califican. No sugerir que sí. |
| Tasas competitivas | No posicionarse como "tasa más baja". Diferenciador = acompañamiento + seguridad + pie bajo. |
| Cuotas fijas / IPC | UNIDAD cobra cuotas fijas. No mencionar IPC como variable. |
| Género ejecutivas | Siempre "ejecutiva" (femenino). Nunca "ejecutivo financiero" masculino. |
| Sitio oficial | Solo `unidadcreditos.cl`. Nunca `creditosunidad.com` (sitio fraudulento con alerta CMF). |
| **CMF — REGLA CRÍTICA** | UNIDAD **NO** está registrada en la CMF ni opera bajo supervisión CMF. La CMF supervisa bancos, no financieras de crédito automotriz. UNIDAD opera bajo Ley N°19.496 y es fiscalizable por SERNAC. Nunca escribir "UNIDAD está en la CMF". |
| "Sujeto a evaluación" | Debe aparecer en toda mención de condiciones, cuotas o aprobación. |
| Títulos anti-fraude | No usar "estafa" ni "fraude" en títulos. Usar "verificar", "compra segura". |

### 2. Normativa automotriz en Chile (fuentes oficiales: Ley de Tránsito, autofact.cl/blog, chileatiende.cl)

| Dato | Regla verificada |
|---|---|
| Revisión técnica — frecuencia | **Anual** para autos particulares livianos. Los autos 0 km tienen 2 años de gracia (Certificado de Homologación) → luego **anual**. Nunca decir "cada 2 años" para autos usados. |
| Revisión técnica — semestral | Solo taxis, transporte escolar, buses, camiones >1.750 kg, GLP/GNC, vehículos anteriores a sep-1992 en RM. |
| Revisión técnica — calendario | Mes de vencimiento = último dígito de patente (ej: patente termina en 7 → vence en octubre). |
| Permiso de circulación | Anual, primer trimestre del año. |
| SOAP | Seguro obligatorio, renovación anual. |
| Prenda | Impide transferencia hasta alzamiento. Verificable en Registro Civil. |
| Multas y anotaciones | Verificables en registrocivil.cl. |
| Tasa máxima convencional | Regulada por CMF. Ninguna financiera puede cobrarla por sobre ese límite. Fuente: cmfchile.cl. |

### 3. Datos técnicos de vehículos (fuentes: ficha oficial marca + autocosmos.cl + chileautos.cl)

Para cada modelo cubierto en un artículo, verificar:
- **Motor**: cilindrada, potencia HP, torque — contrastar con ficha oficial de la marca o autocosmos.cl
- **Versiones disponibles en Chile**: LS, LT, LTZ, etc. — confirmar que la versión mencionada existió/existe en Chile
- **Consumo**: ciudad vs. ruta vs. mixto son valores distintos. **No mezclarlos.** Fuente: autocosmos.cl (ficha técnica oficial)
- **Año de llegada a Chile**: verificar con noticias de lanzamiento o autocosmos/chileautos
- **Transmisiones disponibles por año**: manual / automático / CVT — no asumir

#### Errores frecuentes a vigilar
- Citar consumo "en ciudad" con el valor mixto (error común: mezclar 14-16 km/l mixto con ciudad, cuando ciudad real es ~10-11 km/l).
- Afirmar que una versión (ej: LTZ) existía en un año en que no estaba disponible en Chile.
- Asignar motor incorrecto a un rango de años.

### 4. Datos de mercado de precios (fuentes: chileautos.cl, kavak.com, autocosmos.cl guía de precios)

- Los rangos de precio deben basarse en publicaciones **activas al momento de escribir**, no en precios históricos o inventados.
- Siempre citar la fuente y la fecha: `(Chileautos.cl, [mes año])`.
- Los precios de autos nuevos ($) deben citarse de la marca o autocosmos (precios de lista).
- **No publicar cuotas estimadas** (ver punto 1).

---

## Flujo de trabajo

```
Artículo generado por agente 02
        ↓
Agente 06 ejecuta checklist (secciones 1→4)
        ↓
¿Errores encontrados?
   ├── SÍ → Producir reporte de correcciones (ver formato abajo)
   │         → Devolver al agente 02 para corrección
   │         → Verificar correcciones antes de aprobar
   └── NO → Marcar artículo como "aprobado revisión técnica"
```

## Formato del reporte de correcciones

```markdown
## Reporte de revisión técnica — [nombre del artículo]
Fecha: [fecha]
Revisor: Agente 06

### Errores críticos (bloquean publicación)
| # | Ubicación en artículo | Texto original | Error | Corrección | Fuente |
|---|---|---|---|---|---|

### Errores menores (corregir antes de publicar)
| # | Ubicación | Texto original | Corrección | Fuente |
|---|---|---|---|---|

### Advertencias (verificar con cliente)
- [Lista de puntos a confirmar]

### Estado: ❌ NO APROBADO / ✅ APROBADO CON CORRECCIONES / ✅ APROBADO
```

---

## Fuentes oficiales de referencia rápida

| Tema | Fuente | URL |
|---|---|---|
| Revisión técnica calendario | Autofact | https://www.autofact.cl/blog/mi-auto/revision-tecnica/calendario-2019 |
| Revisión técnica autos nuevos | Autofact | https://www.autofact.cl/blog/mi-auto/revision-tecnica/revision-tecnica-autos-nuevos |
| Fichas técnicas autos Chile | Autocosmos | https://www.autocosmos.cl/catalogo |
| Fichas técnicas autos Chile | Chileautos | https://www.chileautos.cl |
| Tasa máxima convencional | CMF Chile | https://www.cmfchile.cl |
| Verificar anotaciones vehículo | Registro Civil | https://www.registrocivil.cl |
| Normativa tránsito | ChileAtiende | https://www.chileatiende.cl |
| Ficha oficial Chevrolet Chile | Chevrolet.cl | https://www.chevrolet.cl/catalogo |
| Productos UNIDAD | KB interna | `00-contexto/productos.md` |
| Reglas de contenido | KB interna | `AGENTS.md` + `knowledge-base/` |

---

## Notas de sesión (errores ya encontrados — jun 2026)

Ver `01-inteligencia-mercado/outputs/reporte-correcciones-jun2026.md` para el detalle completo de los errores encontrados en los artículos publicados en junio 2026 y sus correcciones.
