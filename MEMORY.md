# MEMORY.md — OffsideVentures (durable facts)

Concise, durable project memory. Operational detail is in `CLAUDE.md`;
requirements in `PRD.md`; live task status in `ROADMAP.md`.

## Identity & goal
- **OffsideVentures**: agentic‑AI‑first, generalized **B2B sales CRM**.
- SvelteKit frontend + Django (Ninja) backend. `OffsideCRM-base/` = vendored Twenty,
  **inspiration only** (no AGPL copying).

## Binding decisions (from discovery — see `spec/`)
- **D1 Backend:** prune freight/logistics models; implement CRM models + API + admin
  the frontend needs in Django; preserve a great Unfold admin; rename → OffsideVentures.
- **D2 Vertical:** generalized B2B sales CRM (Companies / Contacts / Deals / Pipeline).
- **D3 AI:** AI endpoints live on Django; provider keys stored **server‑side only**;
  frontend calls the Django AI endpoints.
- **D4 Design:** premium‑minimal, Linear‑grade, **dark‑mode default**; no purple/indigo/
  violet → **Monochrome + Signal Red** (`#0B0C0E`/`#141518`/`#1C1F23`, accent `#E5484D`).
- **D5 Migrations:** fresh reset (new `0001_initial`).
- **D6 Rename:** full — folders `_OffsideVentures-*`, Django package `uderzoai → offsideventures`, branding.
- **D7 AI provider:** provider‑agnostic (Anthropic + OpenAI via env; `mock` default).

## Status snapshot
- ✅ Done: M0 restructure/rename, M1–M4 backend, M5 design system, M6 app shell, M7 auth+API+mock.
- 🟢 Frontend verified on‑device in **mock mode** (`pnpm dev`, routes 200, BFF proxy + guard work).
- ⚠️ Backend **coded + syntax‑checked, not run** here (no Python env) — run `makemigrations core` first.
- ⬜ Next: **M8/E8 real CRM screens**, then E9 AI UX, E11 tests/CI, E12 docs/deploy.

## Key facts / conventions
- Backend package = `offsideventures` (`DJANGO_SETTINGS_MODULE=offsideventures.settings`; gunicorn `offsideventures.wsgi:application`). Dev DB = SQLite (`DEVELOPMENT_MODE=True`).
- Demo login: `demo@offsideventures.com` / `offside1234` (from `seed_demo`).
- Frontend BFF: browser → same‑origin `/api/*` (SvelteKit proxy) → Django with JWT in **httpOnly cookies**. No CORS needed. Mock mode via `PUBLIC_MOCK=1`.
- Zod schemas in `lib/api/schemas.ts` are the frontend's typed contract. Use semantic Tailwind tokens, not raw hex. Svelte 5 runes; no `any`.

## Gotchas
- **`git push` blocked**: Mapbox token still in commit `ee824999` → scrub history first (roadmap `E0‑S2‑T3`).
- `pnpm install` may need `pnpm approve-builds` (esbuild). Frontend prod → switch `adapter-auto` → `adapter-node`.
- `requirements.txt` carries legacy deps (harmless).
