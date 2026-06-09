# ClickUp — conector MCP (tareas y calendario editorial)

> Estado: 🔑 requiere OAuth en Cursor · Servidor oficial: `https://mcp.clickup.com/mcp`
> Docs ClickUp: [Connect an AI assistant](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server-1) · [Tools soportados](https://developer.clickup.com/docs/mcp-tools)

## Para qué lo usamos en UNIDAD

- **Backlog de growth**: briefs, artículos, investigación de tendencias, vigilancia de competencia.
- **Calendario editorial**: tareas con fecha, estado y responsable.
- **Salida de agentes**: cuando un agente termina (tendencias, SEO, competencia), crear/actualizar tarea en ClickUp con enlace al entregable del repo.

## Configuración en Cursor

### Opción A — Plugin (recomendada)

1. Instalar **ClickUp** desde [Cursor Marketplace](https://cursor.com/marketplace) (ya hecho).
2. Verificar que en **Settings → MCP** aparece `clickup` apuntando a `https://mcp.clickup.com/mcp`.

### Opción B — Manual (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "clickup": {
      "url": "https://mcp.clickup.com/mcp"
    }
  }
}
```

Guardar y **reiniciar Cursor** (una sola ventana abierta).

## Autenticación OAuth (paso crítico)

El plugin instala el servidor, pero **tú debes autorizar** con tu cuenta ClickUp:

1. Abre **Cursor → Settings → MCP**.
2. En `clickup`, pulsa **Connect** / **Login** (o **Needs login**).
3. Se abre el navegador → inicia sesión en ClickUp y **autoriza** el workspace correcto (Skalling / UNIDAD).
4. Vuelve a Cursor y confirma que el estado pasa a **Connected** (verde).

### Si falla o queda en "Authenticating…"

1. `Ctrl+Shift+P` → **Cursor: Clear All MCP Tokens**
2. Cierra ventanas extra de Cursor (deja **solo una**).
3. Repite Connect en MCP.
4. Si persiste: desinstala el plugin ClickUp, reinicia Cursor, reinstala desde Marketplace.

### Verificar desde el chat

Cuando esté conectado, pídele al asistente:

> "Lista la jerarquía de mi workspace en ClickUp y busca tareas de UNIDAD"

Debería poder usar herramientas como **Get Workspace Hierarchy** y **Search Workspace**.

## Mapeo propuesto (rellenar tras la primera conexión)

Copia `clickup-config.example.yaml` → `clickup-config.yaml` (este último está en `.gitignore`) y completa IDs reales:

| Flujo repo | Lista ClickUp sugerida | Trigger |
|---|---|---|
| Agente 01 — tendencias | `Inteligencia / Tendencias` | Semanal (lunes) |
| Agente 02 — brief + artículo | `Contenido / Backlog SEO` | Por cluster |
| Agente 03 — competencia | `Inteligencia / Competencia` | Quincenal |
| Revisión humana | `Contenido / En revisión` | PR abierto |
| Publicado | `Contenido / Publicado` | Merge a main |

Campos útiles en cada tarea:

- **Título**: `[Cluster N] keyword principal`
- **Descripción**: enlace al archivo en GitHub + resumen + CTA
- **Tags**: `unidad`, `cluster-1`, `seo`, `borrador`
- **Custom field** (opcional): `slug`, `estado`, `PR`

## Automatización (siguiente fase)

Una vez OAuth OK, el asistente puede:

1. Ejecutar agente → generar markdown en `01-inteligencia-mercado/outputs/` o `03-contenido/`.
2. **Create Task** en la List correspondiente con el resumen y link al PR.
3. **Update Task** al mergear (estado → listo para publicar en Wix).

> No commitear tokens ni `clickup-config.yaml` con IDs sensibles si el repo es compartido; usar el `.example` en git.

## Troubleshooting

| Síntoma | Causa probable | Acción |
|---|---|---|
| MCP "errored" en el proyecto | OAuth incompleto o token expirado | Clear tokens + reconnect |
| "No MCP servers available" en agente | Servidor no cargado en sesión | Reload window + verificar MCP verde |
| Agente no ve tareas | Workspace equivocado autorizado | Re-auth eligiendo el workspace correcto |
| 401 después de horas | Token expirado (bug conocido Cursor) | Logout del MCP + Connect de nuevo |
