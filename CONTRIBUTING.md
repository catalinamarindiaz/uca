# Cómo colaborar en este repo

Guía para trabajar en equipo (humanos + asistentes de IA como Cursor y Claude) sobre `agilerod/unidad_creditos_contenido`.

> Antes de empezar, lee **[AGENTS.md](./AGENTS.md)**: contexto, reglas de marca y estructura.

## Flujo de trabajo (GitHub Flow)

1. **Sincroniza** `main`:
   ```bash
   git checkout main && git pull
   ```
2. **Crea una rama** por tarea (no trabajes directo en `main`):
   ```bash
   git checkout -b feat/nombre-corto      # nueva funcionalidad/herramienta
   git checkout -b content/slug-articulo  # contenido nuevo
   git checkout -b fix/que-arreglas        # corrección
   ```
3. **Commitea** con mensajes claros (Conventional Commits, en español):
   - `feat:` nueva funcionalidad · `fix:` corrección · `docs:` documentación
   - `content:` artículo/brief · `chore:` mantenimiento · `refactor:` reestructura
4. **Push** y abre un **Pull Request** hacia `main`:
   ```bash
   git push -u origin <tu-rama>
   gh pr create --fill --base main
   ```
5. **Revisión**: el otro colaborador (o tú) revisa el PR. Al aprobar, **merge** (preferir *squash*).

## Reglas para evitar conflictos
- **Una tarea por rama / PR**; PRs pequeños y enfocados.
- Coordinar quién toca qué carpeta cuando trabajen en paralelo (ver tabla en AGENTS.md).
- Hacer `git pull --rebase` antes de pushear si `main` avanzó.
- Resolver conflictos en local; ante la duda, conversar.

## Convenciones de contenido
- Artículos en `03-contenido/articulos/` con front-matter (`title`, `meta_description`, `slug`, `keyword_principal`, `estado`).
- Briefs en `03-contenido/briefs/`.
- Entregables de inteligencia (tendencias, competencia) en `01-inteligencia-mercado/outputs/`.
- Cumplir SIEMPRE las reglas de marca/cumplimiento de AGENTS.md.

## Seguridad
- **Nunca** commitear API keys, tokens ni `.env`. Usar placeholders (`.cursor/mcp.example.json`).
- Si subiste un secreto por error, rotarlo de inmediato y avisar.

## Scripts (entorno)
- Python 3.8+ (los conectores usan solo biblioteca estándar).
- Opcional: `pip install -r requirements.txt` (solo para `pytrends`).
- Probar antes de PR:
  ```bash
  python 04-conectores/scripts/tendencias.py --fuentes news prensa --dias 7
  ```

## Asistentes de IA
- Cursor lee `.cursor/rules/` + `AGENTS.md`. Claude lee `CLAUDE.md` → `AGENTS.md`.
- Mantener `AGENTS.md` actualizado es responsabilidad de quien cambie estructura o reglas.
