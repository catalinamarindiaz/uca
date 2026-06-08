# Growth Digital — Unidad Crédito Automotriz

> **Repo oficial:** [`agilerod/unidad_creditos_contenido`](https://github.com/agilerod/unidad_creditos_contenido) (privado).
> Único repositorio del proyecto de contenido/growth de Unidad Créditos. No mezclar con otros proyectos.

Repositorio de inteligencia y operación para el crecimiento digital de **UNIDAD® Crédito Automotriz** ([unidadcreditos.cl](https://www.unidadcreditos.cl/)), **cliente de Skalling — Aceleración Digital** ([skalling.com](https://www.skalling.com)), que gestiona este trabajo.

> Nota: el MCP `skalling-wordpress` apunta al sitio de la **agencia** (skalling.com), no al sitio del cliente Unidad Créditos.

Este repo es la **base de conocimiento + configuración de agentes de IA** para ejecutar growth de forma sistemática: investigación de tendencias, SEO/contenidos, vigilancia de competencia y monitoreo de fuentes.

## Estructura

```
.
├── README.md                     ← este archivo
├── knowledge-base/               ← qué sabemos (contexto, mercado, fuentes)
│   ├── 01-perfil-unidad-creditos.md
│   ├── 02-productos-oferta.md
│   ├── 03-buyer-personas.md
│   ├── 04-analisis-competencia.md
│   ├── 05-fuentes-de-datos.md     ← validación de acceso a Trends, prensa, Autofact
│   ├── 06-estrategia-growth.md
│   └── 07-seo-keywords-clusters.md
├── agents/                       ← agentes de IA (qué hace cada uno, inputs/outputs)
│   ├── README.md
│   ├── 01-research-tendencias.md
│   ├── 02-seo-contenidos.md
│   ├── 03-vigilancia-competencia.md
│   ├── 04-social-community.md
│   └── fuentes.yaml               ← fuentes en formato legible por máquina
├── scripts/
│   └── trends_cl.py               ← extractor de Google Trends (Chile), sin dependencias
└── .cursor/rules/
    └── contexto-unidad-creditos.mdc  ← contexto persistente para el agente
```

## Cómo usar este repo

1. **Contexto**: el agente de Cursor carga `.cursor/rules/contexto-unidad-creditos.mdc` automáticamente. Empieza por ahí.
2. **Operar un agente**: abre la ficha del agente en `agents/` y pídele al asistente que "ejecute el agente X". Cada ficha define objetivo, fuentes, pasos y formato de salida.
3. **Datos en vivo**: corre `python scripts/trends_cl.py` para tendencias de búsqueda de Chile, y revisa `knowledge-base/05-fuentes-de-datos.md` para el resto de fuentes.

## Herramientas conectadas (MCP)

| Servidor | Estado | Uso en growth |
|---|---|---|
| **skalling-wordpress** | ✅ Activo | Edición de skalling.com (Divi), WPForms (leads), Rank Math (SEO), medios, taxonomías |
| **gtm** (Google Tag Manager) | 🔑 Requiere autenticar | Tracking, eventos de conversión, píxeles |
| **clickup** | 🔑 Requiere autenticar | Gestión de tareas, calendario editorial, backlog de growth |

> Para activar GTM y ClickUp hay que completar la autenticación (ver `knowledge-base/05-fuentes-de-datos.md`).

## Nota importante de marca / seguridad

El sitio oficial es **unidadcreditos.cl**. Existe una alerta de la CMF por un sitio fraudulento (`creditosunidad.com`). Todo contenido debe reforzar señales de confianza y el mensaje "UNIDAD® nunca te pedirá transferencias de dinero".
