# OffsideVentures — Roadmap (Epics · Stories · Tasks)

This roadmap decomposes [`PRD.md`](./PRD.md) into **Milestones**, with a strict
**1:1 mapping between each Milestone and one Epic**. Every PRD requirement maps
to a Story and Task below.

> Status legend: ⬜ not started · 🟡 in progress · ✅ done · ⏸️ blocked/deferred · 🟢 verified on-device

**IDs:** `E{n}` epic · `E{n}-S{m}` story · `E{n}-S{m}-T{k}` task.

## Milestone ↔ Epic map (1:1)

| Milestone | Epic | Title | Status |
|---|---|---|---|
| **M0** | **E0** | Repository Restructure & Rename | ✅ done |
| **M1** | **E1** | Backend — CRM Data Model & Migrations | ✅ done |
| **M2** | **E2** | Backend — CRM REST API (Ninja) | ✅ done |
| **M3** | **E3** | Backend — Agentic AI Endpoints | ✅ done |
| **M4** | **E4** | Backend — Admin Experience (Unfold) | ✅ done |
| **M5** | **E5** | Frontend — Foundation & Design System | ✅ done |
| **M6** | **E6** | Frontend — App Shell & Navigation | ✅ done |
| **M7** | **E7** | Frontend — Auth & API Integration (BFF) | ✅ done |
| **M8** | **E8** | Frontend — CRM Screens | ⬜ not started |
| **M9** | **E9** | Frontend — Agentic AI UX | ⬜ not started |
| **M10** | **E10** | Frontend — Global Search & Command Palette | ⬜ not started |
| **M11** | **E11** | Quality, Testing & CI | ⬜ not started |
| **M12** | **E12** | Docs, Deployment & Launch Readiness | ⬜ not started |

---

## M0 / E0 — Repository Restructure & Rename ✅
*PRD: §3 (D1, D5, D6), §4. Goal: a clean, renamed monorepo.*

- **E0‑S1** Rename to OffsideVentures ✅
  - E0‑S1‑T1 ✅ Rename folders `_OffsideCRM-* → _OffsideVentures-*`.
  - E0‑S1‑T2 ✅ Rename Django package `uderzoai → offsideventures` (manage/wsgi/asgi/settings/urls).
  - E0‑S1‑T3 ✅ Update branding (admin headers, SITE_NAME, API title).
  - E0‑S1‑T4 ✅ Fix `wsgi.py` env‑dump security bug.
- **E0‑S2** Repo hygiene ✅
  - E0‑S2‑T1 ✅ Root `.gitignore` (Node + Python/Django, secrets, anchored build dirs).
  - E0‑S2‑T2 ✅ Retain `OffsideCRM-base/` as inspiration‑only reference.
  - E0‑S2‑T3 ⏸️ **Carry‑over (blocking push):** scrub Mapbox secret from commit `ee824999` before push.

## M1 / E1 — Backend CRM Data Model & Migrations ✅
*PRD: §5, §3 (D2, D5).*

- **E1‑S1** CRM models ✅ — Company, Contact, Pipeline, Stage, Deal, Task, Note, Activity, AgentAction; keep CustomUser/Profile/BlacklistedAccessToken.
  - E1‑S1‑T1 ✅ Remove freight/real‑estate/marketplace models.
  - E1‑S1‑T2 ✅ Add CRM core models + `TimeStampedModel`.
  - E1‑S1‑T3 ✅ Generalize `Company`; slim `Profile`.
- **E1‑S2** Migrations reset ✅
  - E1‑S2‑T1 ✅ Delete legacy migrations (keep `__init__`).
  - E1‑S2‑T2 ⏸️ Generate fresh `0001_initial` (`makemigrations core` — needs Python env).

## M2 / E2 — Backend CRM REST API (Ninja) ✅
*PRD: §6.*

- **E2‑S1** Resource CRUD ✅ — companies, contacts, pipelines/stages, deals, tasks, notes, activities.
  - E2‑S1‑T1 ✅ Ninja schemas (out/in/patch) + label resolvers.
  - E2‑S1‑T2 ✅ Routers with pagination, `?search=`, `?ordering=`, filters.
  - E2‑S1‑T3 ✅ `GET /api/me`, owner‑default on create.
- **E2‑S2** Search & auth ✅
  - E2‑S2‑T1 ✅ `GET /api/search/?q=`.
  - E2‑S2‑T2 ✅ Keep JWT (SimpleJWT/Djoser); fix serializers (drop driver fields).
- **E2‑S3** Verification ⏸️
  - E2‑S3‑T1 ⏸️ Run server, exercise endpoints via `/api/docs` (needs Python env).

## M3 / E3 — Backend Agentic AI Endpoints ✅
*PRD: §7, §3 (D3, D7).*

- **E3‑S1** Provider‑agnostic LLM service ✅ — `anthropic | openai | mock`, keys server‑side.
- **E3‑S2** AI endpoints ✅ — assistant, summarize, draft‑email, score‑lead, classify, suggest‑task.
- **E3‑S3** Human confirm + audit ✅ — `AgentAction` log; `/actions`, `/actions/{id}/apply|reject`.
- **E3‑S4** Config ✅ — settings + `.env.example` for `AI_PROVIDER/AI_MODEL/keys`.
- **E3‑S5** Verification ⏸️ — run against a real provider key.

## M4 / E4 — Backend Admin Experience (Unfold) ✅
*PRD: §4 (preserve great admin UX).*

- **E4‑S1** Unfold ModelAdmin for all CRM models ✅ — list_display, search, filters, autocompletes.
- **E4‑S2** User admin ✅ — Unfold + Django `UserAdmin` for `CustomUser`.

---

## M5 / E5 — Frontend Foundation & Design System ✅
*PRD: §8, §9.*

- **E5‑S1** 🟢 Scaffold project
  - E5‑S1‑T1 🟢 SvelteKit + TS (strict) + Vite + pnpm in `_OffsideVentures-frontend-sveltekit`.
  - E5‑S1‑T2 🟢 Tailwind v4 + PostCSS; ESLint + Prettier + `svelte-check`; scripts.
  - E5‑S1‑T3 🟢 `app.css` design tokens (Monochrome + Signal Red, dark‑first; light tokens scaffolded).
- **E5‑S2** ✅ UI primitives (`lib/components/ui`)
  - E5‑S2‑T1 ✅ Button, Input, Select, Textarea, Checkbox, Badge, Avatar, Label.
  - E5‑S2‑T2 ✅ DataTable (sortable, configurable columns), Card, Tabs, Menu/Dropdown, Tooltip, Toaster.
  - E5‑S2‑T3 ✅ Dialog & Drawer/Slide‑over (bits‑ui), Command‑palette shell.
  - E5‑S2‑T4 ✅ EmptyState / Skeleton (loading) / ErrorState.
- **E5‑S3** ✅ Foundations
  - E5‑S3‑T1 ✅ Icon wrapper (lucide-svelte), typography scale, spacing, focus‑visible.
  - E5‑S3‑T2 🟢 `lib/types` base types; `lib/utils` (format, dates, currency).

## M6 / E6 — Frontend App Shell & Navigation ✅
*PRD: §10 (app shell).*

- **E6‑S1** ✅ Layout
  - E6‑S1‑T1 ✅ `(app)` route group + layout; responsive grid (sidebar + content).
  - E6‑S1‑T2 ✅ Left sidebar object nav (Dashboard, Companies, People, Deals, Tasks, Notes, AI, Settings).
  - E6‑S1‑T3 ✅ Top bar: search→command-palette, **Ask AI** launcher (slide-over), user menu.
- **E6‑S2** ✅ Navigation behavior
  - E6‑S2‑T1 ✅ Active states, ⌘K keyboard, mobile nav drawer, desktop collapsible sidebar.

## M7 / E7 — Frontend Auth & API Integration (BFF) ✅
*PRD: §8, §11.*

- **E7‑S1** 🟢 API client
  - E7‑S1‑T1 🟢 Typed `lib/api` client + **Zod** schemas mirroring backend payloads.
  - E7‑S1‑T2 🟢 SvelteKit **server proxy** (`/api/[...path]`); Django base URL server-only.
- **E7‑S2** ✅ Auth (mock 🟢 verified; Django JWT path coded, pending live verify)
  - E7‑S2‑T1 ✅ `(auth)/login` form action → JWT via BFF; **httpOnly cookies**.
  - E7‑S2‑T2 ✅ `(app)` layout `load` guard; token refresh on 401; logout (blacklist).
  - E7‑S2‑T3 ✅ `GET /api/me` hydration → topbar user; auth error handling.
- **E7‑S3** 🟢 Mock mode
  - E7‑S3‑T1 🟢 `PUBLIC_MOCK` flag + in-memory fixtures + mock router (runs with no backend).

## M8 / E8 — Frontend CRM Screens ⬜
*PRD: §10.*

- **E8‑S1** ⬜ Dashboard
  - E8‑S1‑T1 ⬜ Pipeline value, deals‑by‑stage, open tasks, recent activity, AI prompts.
- **E8‑S2** ⬜ Companies
  - E8‑S2‑T1 ⬜ List: table, configurable columns, search/sort/filter, pagination.
  - E8‑S2‑T2 ⬜ Detail: fields + inline edit, related contacts/deals/tasks/notes, timeline.
  - E8‑S2‑T3 ⬜ Create/edit via drawer/modal.
- **E8‑S3** ⬜ People/Contacts — list + detail (mirror Companies; company link).
- **E8‑S4** ⬜ Deals
  - E8‑S4‑T1 ⬜ **Kanban** pipeline by stage with drag‑to‑move; table toggle.
  - E8‑S4‑T2 ⬜ Deal detail: fields, stage control, links, timeline.
- **E8‑S5** ⬜ Tasks — list/board by status; create/edit; due/priority/assignee/links.
- **E8‑S6** ⬜ Notes & Activity — capture notes; per‑record + global activity feed.
- **E8‑S7** ⬜ Settings — profile; workspace/members/roles (read‑only placeholders).
- **E8‑S8** ⬜ States — polished loading/empty/error across all screens; responsive; a11y.

## M9 / E9 — Frontend Agentic AI UX ⬜
*PRD: §7, §10 (AI).*

- **E9‑S1** ⬜ Assistant surface
  - E9‑S1‑T1 ⬜ Global AI launcher → slide‑over panel + dedicated `/app/ai` page.
  - E9‑S1‑T2 ⬜ Chat UI (streaming‑ready), context chips ("this company/contact/deal").
- **E9‑S2** ⬜ Context actions on detail pages
  - E9‑S2‑T1 ⬜ "Ask AI about this record"; suggested actions (summarize, draft email, create task, score lead, enrich, classify).
- **E9‑S3** ⬜ Human‑in‑the‑loop
  - E9‑S3‑T1 ⬜ Confirm UI before any write; distinct styling for AI suggestion vs committed data.
  - E9‑S3‑T2 ⬜ Agent **audit trail** view (AgentAction list, apply/reject).

## M10 / E10 — Global Search & Command Palette ⬜
*PRD: §10 (global search, ⌘K).*

- **E10‑S1** ⬜ Command palette
  - E10‑S1‑T1 ⬜ ⌘K palette: fuzzy nav + entity results via `/api/search`.
  - E10‑S1‑T2 ⬜ Run actions (create record, invoke AI) from the palette.

## M11 / E11 — Quality, Testing & CI ⬜
*PRD: §12.*

- **E11‑S1** ⬜ Tests
  - E11‑S1‑T1 ⬜ Vitest + Testing Library unit tests for primitives/features.
  - E11‑S1‑T2 ⬜ Playwright e2e for login + core flows.
- **E11‑S2** ⬜ Static quality
  - E11‑S2‑T1 ⬜ `svelte-check`, ESLint, Prettier pass; no `any`.
  - E11‑S2‑T2 ⬜ a11y checks (focus, roles, labels, reduced‑motion).
- **E11‑S3** ⬜ CI
  - E11‑S3‑T1 ⬜ CI‑ready scripts (lint, typecheck, test, build) for frontend + backend.

## M12 / E12 — Docs, Deployment & Launch Readiness ⬜
*PRD: §13.*

- **E12‑S1** ⬜ Docs
  - E12‑S1‑T1 ⬜ Frontend README (setup/dev/env) — backend README already ✅.
  - E12‑S1‑T2 ⬜ Root README tying backend + frontend together; update PRD/ROADMAP statuses.
- **E12‑S2** ⬜ Deployment
  - E12‑S2‑T1 ⬜ SvelteKit adapter + env strategy (`PUBLIC_*` vs server‑only).
  - E12‑S2‑T2 ⬜ Backend: `makemigrations`/`migrate`/`seed_demo`; update DO run command to `offsideventures.wsgi`.
  - E12‑S2‑T3 ⏸️ Resolve Mapbox secret history scrub (E0‑S2‑T3) before first push.

---

## Coverage check (PRD → roadmap)

| PRD section | Covered by |
|---|---|
| §1 Goals / §2 Personas | E0–E12 (whole roadmap) |
| §3 Decisions (D1–D7) | E0, E1, E2, E3 |
| §4 Architecture | E0, E5, E7 |
| §5 Data model | E1 |
| §6 API | E2 |
| §7 AI | E3 (backend), E9 (frontend) |
| §8 Frontend architecture | E5, E7 |
| §9 Design system | E5 |
| §10 Pages & UX | E6, E8, E10 |
| §11 Auth & security | E7 |
| §12 Quality | E11 |
| §13 Assumptions/risks | E12 (+ E0‑S2‑T3) |

**Current state:** M0–M4 (backend + restructure) are ✅ done at code level
(written + syntax‑checked); **nothing is 🟢 verified on‑device yet** — the
`makemigrations`/run‑and‑exercise steps are ⏸️ pending a Python runtime, and the
Mapbox history scrub is ⏸️ blocking the first push. M5–M12 (frontend, quality,
deploy) are ⬜ not started. **M5–M7 done** (E7 mock path 🟢 smoke-tested: routes 200, BFF proxy + auth guard work). Next up: **M8 / E8 — CRM Screens**.
