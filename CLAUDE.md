# CLAUDE.md — OffsideVentures

Guidance for Claude Code working in this repository. See `PRD.md` (requirements)
and `ROADMAP.md` (epics/stories/tasks with live status) for the full picture.

## What this is

**OffsideVentures** — an agentic‑AI‑first, generalized **B2B sales CRM**.
- **Frontend:** SvelteKit (Svelte 5 runes) + TypeScript + Vite + Tailwind v4, in
  `_OffsideVentures-frontend-sveltekit/`. Dark‑first "Monochrome + Signal Red" design.
- **Backend:** Django 4.2 + Django Ninja (API) + Django‑Unfold (admin), in
  `_OffsideVentures-backend-django/`. JWT auth (SimpleJWT + Djoser).
- **`OffsideCRM-base/`** is a vendored clone of `twentyhq/twenty` — **design
  inspiration only. Do NOT copy AGPL source, markup, icons, or branding.**

Originally a fork of Twenty; pivoted to a fresh SvelteKit CRM against the existing
Django backend (which was itself pivoted from a freight/logistics app, "FR8 Pro").

## Repository layout

```
OffsideCRM/                              # git repo root (remote: offsideAI/OffsideCRM)
├── _OffsideVentures-backend-django/     # Django API + Unfold admin
├── _OffsideVentures-frontend-sveltekit/ # SvelteKit CRM UI
├── OffsideCRM-base/                     # vendored Twenty — inspiration only
├── PRD.md · ROADMAP.md · README.md
└── spec/                                # screenshots of the discovery decisions
```

## Backend — `_OffsideVentures-backend-django/`

**Run (dev uses SQLite; no Postgres needed):**
```bash
cd _OffsideVentures-backend-django
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations core      # migrations were reset — generate 0001
python manage.py migrate
python manage.py seed_demo                 # demo@offsideventures.com / offside1234
python manage.py createsuperuser           # for /admin
python manage.py runserver                 # http://localhost:8000
```
- API: Django **Ninja** at `/api/` — Swagger `/api/docs`, OpenAPI `/api/openapi.json`.
- Admin: `/admin` (Unfold). Auth: `POST /auth/jwt/create/`, `/auth/users/me/`.
- Django project package is **`offsideventures`** (`DJANGO_SETTINGS_MODULE=offsideventures.settings`,
  gunicorn target `offsideventures.wsgi:application`).

**Structure** (`core/`): `models.py` (CRM data model), `api.py` (Ninja CRM API +
mounts AI router), `schemas.py` (Ninja I/O), `admin.py` (Unfold), `serializers.py`
(Djoser auth), `views.py` (auth helpers + JSON root), `ai/` (provider‑agnostic
LLM service + `/api/ai/*` router), `management/commands/seed_demo.py`.

**Data model:** `Company, Contact, Pipeline, Stage, Deal, Task, Note, Activity,
AgentAction` (AI audit trail) + `CustomUser, Profile, BlacklistedAccessToken`.
Single workspace; owner‑based attribution; address fields embedded on Company.

**AI:** `AI_PROVIDER = anthropic | openai | mock` (default `mock`). Keys
(`ANTHROPIC_API_KEY`/`OPENAI_API_KEY`) are read **server‑side only**. Endpoints:
`/api/ai/{assistant,summarize,draft-email,score-lead,classify,suggest-task}` +
audit trail `/api/ai/actions` with human‑confirm `apply`/`reject`.

**Conventions:** Ninja for the API; DRF/Djoser only for auth; Unfold ModelAdmin
for every model; keep the AI provider abstraction in `core/ai/`.

## Frontend — `_OffsideVentures-frontend-sveltekit/`

**Run (mock mode is the default — no backend required):**
```bash
cd _OffsideVentures-frontend-sveltekit
pnpm install               # if prompted about build scripts: pnpm approve-builds  (esbuild)
cp .env.example .env       # PUBLIC_MOCK=1
pnpm dev                   # http://localhost:5173
```
Scripts: `pnpm dev | build | preview | check | lint | format`.
Verify with `pnpm check` (svelte-check) and `pnpm build`. Node 22 + pnpm.

**Structure** (`src/`):
- `app.css` — design tokens (`:root` vars → Tailwind via `@theme inline`) + base styles.
- `lib/components/ui/` — reusable primitives (Button, Table/DataTable, Dialog, Drawer,
  Menu, Tooltip, CommandPalette, Toaster, EmptyState, …) exported via `index.ts`.
- `lib/components/app/` — shell (Sidebar, NavList, Topbar).
- `lib/api/` — `schemas.ts` (Zod, source of truth) + `client.ts` (browser → BFF).
- `lib/server/` — `config.ts`, `cookies.ts`, `api.ts` (BFF gateway: Django + JWT
  refresh, or mock), `auth.ts`, `mock.ts` (mock router). **Server‑only.**
- `lib/mock/data.ts` — fixtures. `lib/stores/` — `ui.svelte.ts`, `toast.svelte.ts`.
- `routes/` — `/` design showcase; `(auth)/login`; `(app)/app/{dashboard,companies,
  people,deals,tasks,notes,ai,settings}`; `api/[...path]` (BFF proxy); `auth/logout`.

**Auth / API (BFF):** the browser calls same‑origin `/api/*`; the SvelteKit server
proxy attaches the JWT (kept in **httpOnly cookies**) and forwards to Django. The
Django origin is never exposed; **no CORS needed** for proxied calls. Guard lives
in `(app)/+layout.server.ts`.

**Design conventions:** dark‑first, Monochrome + Signal Red. Use **semantic Tailwind
utilities** (`bg-surface-1`, `text-muted`, `border-border`, `bg-accent`, `rounded-lg`),
never raw hex. Svelte 5 idioms (`$props/$state/$derived`, snippets). No `any`.
Zod‑validate at API boundaries. Lucide icons are legacy class components → typed as
`ComponentType` (see `lib/types`).

## Current status (see ROADMAP.md)

- **Done:** M0 restructure/rename, M1–M4 backend (models/API/AI/admin), M5 design
  system, M6 app shell, M7 auth+API+mock.
- **Frontend verified on‑device** in mock mode (routes 200, BFF proxy + auth guard
  work, dashboard shows live stats). Backend is **written + syntax‑checked but not
  run here** (no Python in the authoring env) — run `makemigrations` on first setup.
- **Next:** M8/E8 — real CRM screens (lists/detail/kanban wired to the API), then
  M9/E9 (AI Copilot UX), M11 tests/CI, M12 docs/deploy.
- Record pages currently show "arrives in E8" placeholders; only the dashboard is live.

## Gotchas

- **`git push` is blocked**: an old Mapbox token still exists in commit `ee824999`.
  It must be scrubbed from history (roadmap `E0‑S2‑T3`) before the first push.
- Frontend prod build uses `adapter-auto`; switch to `adapter-node` for self‑host (E12).
- `requirements.txt` still carries some legacy deps (streamlit/folium/…) — harmless, prunable.
- On DigitalOcean, the run command is `offsideventures.wsgi:application` (was `uderzoai`).
