# Growth Digital — Unidad Crédito Automotriz

> **Repo oficial:** [`agilerod/unidad_creditos_contenido`](https://github.com/agilerod/unidad_creditos_contenido) (privado).
> Único repositorio del proyecto de contenido/growth de Unidad Créditos. No mezclar con otros proyectos.

Repositorio de inteligencia y operación para el crecimiento digital de **UNIDAD® Crédito Automotriz** ([unidadcreditos.cl](https://www.unidadcreditos.cl/)), **cliente de Skalling — Aceleración Digital** ([skalling.com](https://www.skalling.com)), que gestiona este trabajo.

> Nota: el MCP `skalling-wordpress` apunta al sitio de la **agencia** (skalling.com), no al sitio del cliente Unidad Créditos.

Este repo es la **base de conocimiento + configuración de agentes de IA** para ejecutar growth de forma sistemática: investigación de tendencias, SEO/contenidos, vigilancia de competencia y monitoreo de fuentes.

## Estructura

```
.
├── README.md
├── 00-contexto/                  ← quiénes somos (empresa, productos, personas)
│   ├── empresa.md
│   ├── productos.md
│   └── buyer-personas.md
├── 01-inteligencia-mercado/      ← qué pasa afuera (competencia, fuentes, outputs)
│   ├── competencia.md
│   ├── fuentes-de-datos.md
│   └── outputs/                  ← entregables de los agentes (tendencias, competencia)
├── 02-estrategia/                ← cómo crecemos
│   ├── growth-strategy.md
│   ├── seo-keywords-clusters.md
│   └── lead-capture-playbook.md  ← estrategias de captación de leads
├── 03-contenido/                 ← entregables de contenido
│   ├── briefs/
│   └── articulos/
├── 04-conectores/                ← capa de datos vivos (MCP + scripts)
│   ├── README.md
│   ├── mcp-registry.yaml         ← inventario de MCPs y su estado
│   ├── google-trends.md          ← cómo conectar Google Trends (MCP + fallback)
│   ├── fuentes.yaml
│   └── scripts/trends_cl.py
├── 05-agentes/                   ← agentes de IA (fichas ejecutables)
│   ├── README.md
│   └── 01..04 (tendencias, SEO, competencia, social)
└── .cursor/
    ├── rules/contexto-unidad-creditos.mdc  ← contexto persistente
    └── mcp.example.json                    ← ejemplo de config MCP (Trends)
```

## Cómo usar este repo

1. **Contexto**: el agente de Cursor carga `.cursor/rules/contexto-unidad-creditos.mdc` automáticamente. Empieza por ahí.
2. **Operar un agente**: abre la ficha en `05-agentes/` y pide "ejecuta el agente X". Cada ficha define objetivo, fuentes, pasos y formato de salida.
3. **Datos en vivo**: la carpeta `04-conectores/` define cómo se conecta cada fuente. Para tendencias rápidas: `python 04-conectores/scripts/trends_cl.py`; para datos por keyword: MCP de Trends (ver `04-conectores/google-trends.md`).
4. **Captación de leads**: la estrategia operativa está en `02-estrategia/lead-capture-playbook.md`.

## Herramientas conectadas (MCP)

| Servidor | Estado | Uso en growth |
|---|---|---|
| **skalling-wordpress** | ✅ Activo | Edición de skalling.com (Divi), WPForms (leads), Rank Math (SEO), medios, taxonomías |
| **gtm** (Google Tag Manager) | 🔑 Requiere autenticar | Tracking, eventos de conversión, píxeles |
| **clickup** | 🔑 Requiere autenticar | Gestión de tareas, calendario editorial, backlog de growth |

> Para activar GTM y ClickUp hay que completar la autenticación. El MCP de Google Trends (trendsmcp.ai) se añade aparte (ver `04-conectores/google-trends.md`). Estado y uso de cada MCP en `04-conectores/mcp-registry.yaml`.

## Nota importante de marca / seguridad

El sitio oficial es **unidadcreditos.cl**. Existe una alerta de la CMF por un sitio fraudulento (`creditosunidad.com`). Todo contenido debe reforzar señales de confianza y el mensaje "UNIDAD® nunca te pedirá transferencias de dinero".
