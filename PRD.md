# OffsideVentures — Product Requirements Document (PRD)

> **Status:** Living document · **Version:** 1.0 (v1 MVP) · **Owner:** OffsideAI
> **Repository:** `offsideAI/OffsideCRM` (product name: **OffsideVentures**)

OffsideVentures is an **Agentic‑AI‑first CRM** for founders, agencies, B2B teams,
and service businesses. It pairs a calm, premium, Linear‑grade UI with an AI
copilot that is native to the product — able to summarize records, draft
outreach, score leads, classify inbound, and propose CRM changes that a human
confirms before anything is written.

This PRD captures the **entire** requirement set and every decision made during
discovery (the four structured decisions recorded in `spec/spec_*.png`). It is
the single source of truth; `ROADMAP.md` decomposes it into Epics → Stories →
Tasks with a 1:1 milestone↔epic mapping.

---

## 1. Vision & Goals

**Vision.** A modern, elegant, fast CRM where AI is a first‑class collaborator,
not a bolt‑on — built on a pragmatic, maintainable architecture rather than a
heavy enterprise stack.

**Goals (v1)**
1. A polished, production‑quality CRM frontend (SvelteKit) for a **generalized
   B2B sales** workflow: Companies, Contacts, Deals/Pipeline, Tasks, Notes,
   Activities.
2. A **Django** backend exposing a clean JSON API + premium admin, with the CRM
   data model the frontend needs.
3. **Agentic AI** that feels native: a global assistant, context‑aware actions
   on records, and **human confirmation before any write**.
4. A distinct, premium **dark‑first visual identity** (Monochrome + Signal Red)
   that reads as the work of a top FAANG design team — not "AI‑generated".
5. Secure handling of secrets: **AI provider keys live only on the Django
   server**; the browser never sees them.

**Non‑Goals (v1)**
- Multi‑tenant workspaces (single workspace in v1; designed so it can be added).
- Rebuilding Twenty's full architecture (Twenty is **inspiration only**).
- Billing, email sync, calendar sync, telephony, marketing automation.
- Mobile‑native apps (responsive web only).
- Real outbound email sending (AI *drafts*; sending is out of scope for v1).

**Success metrics**
- A new engineer can run backend + frontend locally in < 15 minutes from the READMEs.
- All MVP screens are navigable, responsive, accessible (WCAG AA baseline), and
  wired to the API with graceful loading/empty/error states.
- The AI copilot answers record questions and proposes actions; every write is
  gated by an explicit human confirm and recorded in an audit trail.
- Lighthouse/Pagespeed: fast first load; no layout shift on list/detail views.

---

## 2. Personas

| Persona | Needs | Primary surfaces |
|---|---|---|
| **Founder / GTM lead** | Pipeline visibility, quick capture, AI leverage | Dashboard, Deals, AI copilot |
| **Account Executive** | Work contacts/deals, log activity, follow‑ups | Companies, Contacts, Deals, Tasks |
| **Agency / service operator** | Client accounts, tasks, notes | Companies, Tasks, Notes |
| **Admin / ops** | Manage data, users, fix records | Django Unfold admin |

Primary vertical for v1 UX and seed data: **Generalized B2B sales CRM**.

---

## 3. Decisions Log (recorded during discovery)

These four decisions (captured in `spec/spec_1..10.png`) are binding for v1:

| # | Decision | Choice |
|---|---|---|
| D1 | **Backend strategy** | Remove inapplicable (freight/real‑estate/marketplace) models; **implement the CRM models, API endpoints, and admin the frontend needs in Django**; preserve a great admin UX; **rename the project to OffsideVentures**. |
| D2 | **Vertical focus** | **Generalized B2B sales CRM** (Companies / Contacts / Deals / Pipeline). |
| D3 | **AI scope** | **Add AI API endpoints on the Django backend**; AI provider keys stored in the **Django environment** (server‑side); the frontend calls the Django AI endpoints. |
| D4 | **Design identity** | **Premium minimal, Linear aesthetic, dark‑mode default**, corporate & polished; **no indigo/violet/purple**; a distinct palette → **Monochrome + Signal Red**. |
| D5 | **Migrations** | **Fresh reset** — drop legacy migrations, generate a new `0001_initial`. |
| D6 | **Rename scope** | **Full** — folders `_OffsideCRM-* → _OffsideVentures-*`, Django package `uderzoai → offsideventures`, and all branding. (`OffsideCRM-base/` retained as the Twenty design‑inspiration reference.) |
| D7 | **AI provider** | **Provider‑agnostic** — Anthropic + OpenAI selectable via env; `mock` default so it runs with no key. |

---

## 4. Repository & System Architecture

```
OffsideCRM/                         # git repo root (product: OffsideVentures)
├── _OffsideVentures-backend-django/   # Django 4.2 + Django Ninja API + Unfold admin
├── _OffsideVentures-frontend-sveltekit/ # SvelteKit + TS + Vite + Tailwind v4 (to build)
├── OffsideCRM-base/                   # Vendored twentyhq/twenty — DESIGN INSPIRATION ONLY
├── PRD.md  ·  ROADMAP.md  ·  README.md
└── spec/                              # decision screenshots (requirements record)
```

- **Backend:** Django 4.2, **Django Ninja** API at `/api/` (auto‑OpenAPI at
  `/api/openapi.json`, Swagger at `/api/docs`), **Django‑Unfold** admin at
  `/admin/`. Auth via **SimpleJWT + Djoser**. SQLite in dev, Postgres in prod.
- **Frontend:** **SvelteKit** (Svelte 5 runes) + TypeScript (strict) + Vite,
  **Tailwind v4** + CSS‑variable design tokens, headless **bits‑ui** primitives.
- **Integration:** the frontend talks to Django **only through SvelteKit server
  routes (BFF proxy)**. JWTs are kept in **httpOnly cookies**; the Django base
  URL is never exposed to the browser. **Zod** validates at API boundaries.
- **AI:** Django `/api/ai/*` endpoints call a **provider‑agnostic** LLM service;
  keys are read from the Django environment only.

**Licensing‑safe use of Twenty.** Study patterns only (sidebar object nav, dense
list/table views, record detail + activity timeline, command palette, kanban
pipeline, calm neutral surfaces). **Do not copy** AGPL source, markup, icons, or
branding. All components, tokens, and icons (Lucide/Tabler) are built fresh.

---

## 5. Data Model (backend — implemented)

Single workspace in v1; record ownership via `owner` FK. All records carry
`created_at`/`updated_at` (via `TimeStampedModel`).

| Model | Key fields |
|---|---|
| **CustomUser** | email (login), username, names, is_active, is_deactivated |
| **Profile** | user 1‑1, role (regular/manager/admin), job_title, phone, avatar_url, bio |
| **Company** | name, domain, industry, size, status (prospect/active/customer/churned), description, phone, email, linkedin_url, logo_url, annual_revenue, address (street/city/state/postal_code/country), owner |
| **Contact** | first_name, last_name, email, phone, job_title, status (lead/active/customer/archived), linkedin_url, company→Company, owner |
| **Pipeline** | name, is_default |
| **Stage** | pipeline→Pipeline, name, order, probability (0–100), is_won, is_lost |
| **Deal** | name, company, primary_contact, pipeline, stage, amount, currency, status (open/won/lost), close_date, description, owner |
| **Task** | title, description, status (todo/in_progress/done), priority (low/medium/high), due_date, completed_at, assignee, links (company/contact/deal) |
| **Note** | body, author, links (company/contact/deal) |
| **Activity** | type (note/call/email/meeting/task/stage_change/system), summary, body, actor, occurred_at, links (company/contact/deal) |
| **AgentAction** | action_type, status (suggested/approved/applied/rejected/failed), prompt, result (JSON), proposed_payload (JSON), target_type/target_id, model, actor — **AI audit trail** |
| **BlacklistedAccessToken** | token_jti, user, created_at (JWT logout revocation) |

Custom fields and multi‑tenant workspaces are **out of v1** but the schema and
UI should not preclude them.

---

## 6. Backend API (implemented)

**Auth.** `POST /auth/jwt/create/` (access+refresh), refresh, blacklist; current
user `GET /auth/users/me/`; logout `POST /api/auth/logout`. Bearer/JWT header.

**CRM (JWT‑auth, under `/api/`).** Each list supports `?search=`, `?ordering=`,
resource filters, and limit/offset pagination (`{items, count}`):

| Resource | Endpoints |
|---|---|
| Me | `GET /api/me` |
| Companies | `GET/POST /api/companies/` · `GET/PATCH/DELETE /api/companies/{id}` |
| Contacts | `GET/POST /api/contacts/` · `GET/PATCH/DELETE /api/contacts/{id}` |
| Pipelines/Stages | `GET/POST /api/pipelines/` · `POST/PATCH/DELETE /api/pipelines/stages[/{id}]` |
| Deals | `GET/POST /api/deals/` · `GET/PATCH/DELETE /api/deals/{id}` |
| Tasks | `GET/POST /api/tasks/` · `PATCH/DELETE /api/tasks/{id}` |
| Notes | `GET/POST /api/notes/` · `DELETE /api/notes/{id}` |
| Activities | `GET/POST /api/activities/` |
| Search | `GET /api/search/?q=` (companies, contacts, deals) |

---

## 7. Agentic AI Requirements

**Server endpoints (`/api/ai/*`, keys server‑side only):**
`assistant` (context‑aware chat), `summarize`, `draft-email`, `score-lead`,
`classify`, `suggest-task`; audit trail `GET /actions`; **human confirm** via
`POST /actions/{id}/apply` and `/actions/{id}/reject`.

**Behavioral requirements**
1. **Global AI assistant** entry point reachable from anywhere.
2. **Context‑aware** panel: "Ask about this company / contact / deal".
3. Natural‑language Q&A over the current record's CRM context.
4. **Suggested actions:** summarize record, generate follow‑up email, create
   task, enrich, score lead, classify opportunity, draft email.
5. **Human confirmation before any destructive or write action.** AI proposals
   are stored as `AgentAction(status=suggested)` and only mutate data on
   explicit `apply`.
6. **Clear distinction** between an AI suggestion and committed CRM data
   (visually and in data — suggestions are never silently written).
7. **Audit trail** of agent actions (the `AgentAction` log; surfaced in‑app).
8. **No key exposure:** the browser calls only Django AI endpoints; provider is
   `anthropic | openai | mock` via env (`mock` returns clearly‑labelled text).

---

## 8. Frontend Architecture (to build)

- **SvelteKit (Svelte 5 runes) + TypeScript (strict, no `any`) + Vite.**
- **Routing:** `(auth)/login`; authenticated group `(app)/app/{dashboard,
  companies, people, deals, tasks, notes, ai, settings}` with detail routes
  (`companies/[id]`, `people/[id]`, `deals/[id]`).
- **API client (`src/lib/api`)** → SvelteKit **server routes as a BFF proxy**;
  JWT in **httpOnly cookies**; **Zod** schemas validate responses; typed clients.
- **State:** SvelteKit `load` + Svelte runes/stores only where needed (no hidden
  global state). Apollo/Recoil not used.
- **Structure:** `lib/components/ui` (primitives), `lib/features/*` (feature
  modules), `lib/api`, `lib/types`, `lib/stores`.
- **Auth guard:** `(app)` layout `load` redirects unauthenticated users to login;
  `(auth)` group for unauthenticated pages.
- **Mock‑data mode:** a flag so the app runs with no backend (realistic mocks).
- **Quality:** Vitest + Testing Library, Playwright e2e, `svelte-check`, ESLint,
  Prettier; CI‑ready scripts; a11y from the start; responsive.
- **Package manager / Node:** pnpm, Node 22 LTS. Docker/devcontainer deferred.

---

## 9. Design System

**Identity:** premium minimal, Linear‑grade, **dark‑mode default**, corporate &
polished. **No indigo/violet/purple.** Accent is a restrained **signal red** used
sparingly (primary action, active nav, focus, key emphasis) — "rare punctuation".

**Palette — Monochrome + Signal Red (dark‑first)**

| Token | Value | Use |
|---|---|---|
| `--surface-0` | `#0B0C0E` | App background |
| `--surface-1` | `#141518` | Cards, sidebar, panels |
| `--surface-2` | `#1C1F23` | Raised elements, inputs, hover |
| `--border` | `#262A2F` | Hairline borders |
| `--text` | `#E8EAEC` | Primary text |
| `--text-muted` | `#9AA0A7` | Secondary text |
| `--accent` | `#E5484D` | Signal red (primary action/active/focus) |
| `--accent-hover` | `#F05A5F` | Accent hover |
| `--success` / `--warning` | calm green / amber | status only, low saturation |

**Principles:** hairline borders over shadows; compact‑but‑readable density;
editorial spacing; typography carries hierarchy (system/grotesk sans + mono for
numerics/IDs); minimal motion (respect `prefers-reduced-motion`). A
**light theme** is structured via tokens for later but dark ships as default.

**Reusable primitives** (in `lib/components/ui`): Button, Input/Select/Textarea,
Table (sortable, configurable columns), Card, Badge/Status pill, Avatar, Dialog,
Drawer/Slide‑over, Dropdown/Menu, Tabs, Tooltip, Toast, Command palette, and
**Empty / Loading (skeleton) / Error** states.

**Anti‑references (reject):** generic SaaS gradient heroes, glassmorphism,
navy+lime, identical bento grids, noisy color, purple "AI" clichés.

---

## 10. Pages & UX (MVP)

| Screen | Requirements |
|---|---|
| **Login** | Email/password → Django JWT via BFF; error states; redirect to app. |
| **App shell** | Left sidebar (object nav), top bar (global search + command‑palette trigger + AI launcher + user menu). |
| **Dashboard** | At‑a‑glance: pipeline value, deals by stage, open tasks, recent activity, AI prompts. |
| **Companies — list** | Dense table, configurable columns, search/sort/filter, pagination, row → detail. |
| **Company — detail** | Header + fields (inline edit), related contacts/deals/tasks/notes, **activity timeline**, **"Ask AI about this company"**. |
| **People/Contacts — list & detail** | As companies; contact↔company link; timeline; AI affordances. |
| **Deals — pipeline** | **Kanban** by stage (drag to move), + table view toggle; deal → detail. |
| **Deal — detail** | Fields, stage control, company/contact links, timeline, AI affordances. |
| **Tasks** | List/board by status; create/edit; due dates, priority, assignee, record links. |
| **Notes / Activity** | Notes capture + activity feed per record and globally. |
| **AI assistant** | Slide‑over panel + dedicated page: chat, context chips, suggested actions, confirm UI, audit trail. |
| **Settings** | Profile, (placeholder) workspace, members/roles surfaced read‑only where applicable. |
| **Global search** | ⌘K command palette: jump to records, run actions, invoke AI. |

**Interaction requirements:** configurable list columns (Twenty‑style); switch
table/kanban/detail where relevant; record detail timeline/activity panels;
inline editing; create/edit via **drawer or modal** (full page only when needed).

---

## 11. Auth & Security

- JWT (access+refresh) obtained from Django; stored in **httpOnly, Secure,
  SameSite cookies** set by the SvelteKit server proxy; access token refreshed
  server‑side; logout blacklists the token.
- Browser never holds the raw JWT or the Django origin; all calls go via BFF.
- **No secrets in client code.** AI provider keys are server‑side env only.
- CORS/CSRF: API is token‑based (CSRF off on the Ninja API); SvelteKit origins
  configured in Django `DJANGO_CORS_ALLOWED_ORIGINS`.
- Roles/permissions surfaced in UI where present; enforcement is server‑side.

---

## 12. Quality Standards

- Small, composable components; explicit types; **no `any`**; no hidden global
  state; semantic HTML + accessible labels; keyboard navigation; respect
  reduced‑motion.
- Test pyramid: unit (Vitest + Testing Library), integration, e2e (Playwright).
  Query by user‑visible text/roles. `svelte-check` + ESLint + Prettier in CI.
- Backend: keep `up`/`down` discipline for any future migrations; never rewrite
  committed migrations; type‑checked schemas at API boundaries.
- Helpful comments only where they clarify non‑obvious decisions; actionable
  TODOs only. App stays runnable after each major step.

---

## 13. Assumptions, Constraints & Risks

- **No Python runtime in the authoring environment** — backend is written and
  syntax‑checked but you run `pip install` + `makemigrations` + `migrate` + `seed_demo`.
- **DigitalOcean deploy:** update the run command to `offsideventures.wsgi:application`
  and the renamed folder paths.
- **Mapbox secret history scrub** remains required before any `git push` — the
  token still exists in commit `ee824999` even though the templates are deleted.
- `requirements.txt` still carries legacy deps (streamlit/folium/faiss…) —
  harmless, prunable later.
- A populated production (freight) DB must be recreated due to the fresh‑reset
  migration decision.

---

## 14. Out of Scope (v1) / Future

Multi‑tenant workspaces · custom fields · email/calendar sync · real email send ·
billing/subscriptions · advanced reporting/dashboards · role‑based field
permissions in UI · import/export · webhooks/integrations marketplace · native
mobile · real‑time collaboration. The architecture should not preclude these.

---

## 15. Open Questions

1. Light theme: ship a toggle in v1 or defer? (Default: dark‑only in v1, tokens ready.)
2. Deployment target for the frontend (Vercel/Node adapter/DO)? (Default: Node adapter.)
3. Should AI `draft-email` ever *send*, or only draft? (v1: draft only.)
4. Preferred default Claude/OpenAI model ids per the account in use (set via `AI_MODEL`).
