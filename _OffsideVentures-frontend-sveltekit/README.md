# OffsideVentures — Frontend (SvelteKit)

The CRM UI for OffsideVentures: SvelteKit (Svelte 5 runes) + TypeScript + Vite +
Tailwind v4, with a dark-first **Monochrome + Signal Red** design system. It talks
to the Django backend through SvelteKit server routes (BFF proxy) — see the PRD.

## Requirements

- Node 22 LTS, pnpm 9+ (`corepack enable`)

## Setup

```bash
cd _OffsideVentures-frontend-sveltekit
pnpm install
cp .env.example .env        # PUBLIC_MOCK=1 runs with no backend
pnpm dev                    # http://localhost:5173
```

## Scripts

| Command | Purpose |
|---|---|
| `pnpm dev` | Vite dev server |
| `pnpm build` / `pnpm preview` | Production build / preview |
| `pnpm check` | `svelte-check` type checking |
| `pnpm lint` / `pnpm format` | ESLint + Prettier check / write |

## Structure

```
src/
├── app.css                 # Design tokens (Monochrome + Signal Red) + base styles
├── app.html · app.d.ts
├── lib/
│   ├── components/ui/       # Reusable primitives (Button, Badge, Card, Input, …)
│   ├── types/               # Shared types
│   └── utils/               # cn(), format helpers
└── routes/
    ├── +layout.svelte       # Loads app.css + web fonts
    └── +page.svelte         # Design-system showcase (temporary landing)
```

## Design tokens

Raw values live on `:root` in `src/app.css` and are mapped to Tailwind utilities
via `@theme inline`, so they stay live for runtime theming (a light theme is
scaffolded under `:root.light`). Use semantic utilities — `bg-surface-1`,
`text-muted`, `border-border`, `bg-accent`, `ring-accent`, `rounded-lg`,
`font-mono` — rather than raw hex.

## Status

This is **M5 / E5** (Foundation & Design System). Upcoming: app shell + routing
(E6), auth + BFF API client (E7), CRM screens (E8), and the agentic AI UX (E9).
See `../ROADMAP.md`.
