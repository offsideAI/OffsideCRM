# OffsideVentures — Backend (Django)

JSON API for the OffsideVentures CRM: a generalized, AI-native B2B sales CRM.
Built with **Django 4.2 + Django Ninja** (API) and **Django-Unfold** (admin).
The user-facing UI is the separate SvelteKit app in `_OffsideVentures-frontend-sveltekit`.

## Stack

- **API:** Django Ninja at `/api/` — OpenAPI at `/api/openapi.json`, Swagger UI at `/api/docs`.
- **Auth:** JWT (SimpleJWT + Djoser). Login `POST /auth/jwt/create/`, refresh, blacklist; current user `GET /auth/users/me/`.
- **Admin:** Django-Unfold at `/admin/`.
- **AI:** provider-agnostic (`anthropic` | `openai` | `mock`); keys are read **server-side only**.

## Setup

```bash
cd _OffsideVentures-backend-django
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then edit values

python manage.py makemigrations core
python manage.py migrate
python manage.py seed_demo      # demo data + demo@offsideventures.com / offside1234
python manage.py createsuperuser
python manage.py runserver
```

> The data model was pivoted from a legacy freight app; migrations were reset, so
> run `makemigrations core` to generate a fresh `0001_initial`.

## Data model

`Company` (account), `Contact` (person), `Pipeline` → `Stage` → `Deal`, plus
`Task`, `Note`, `Activity` (timeline), and `AgentAction` (AI audit trail).
v1 is single-workspace with owner-based record attribution.

## Key endpoints

| Resource | Path |
|---|---|
| Current user | `GET /api/me` |
| Companies | `GET/POST /api/companies/`, `GET/PATCH/DELETE /api/companies/{id}` |
| Contacts | `GET/POST /api/contacts/`, `…/{id}` |
| Pipelines & stages | `GET/POST /api/pipelines/`, `POST/PATCH/DELETE /api/pipelines/stages[/{id}]` |
| Deals | `GET/POST /api/deals/`, `…/{id}` |
| Tasks | `GET/POST /api/tasks/`, `PATCH/DELETE …/{id}` |
| Notes | `GET/POST /api/notes/`, `DELETE …/{id}` |
| Activities | `GET/POST /api/activities/` |
| Search | `GET /api/search/?q=` |

List endpoints support `?search=`, `?ordering=`, resource filters (e.g. `?status=`,
`?company_id=`), and limit/offset pagination (`?limit=&offset=` → `{items, count}`).

## AI endpoints (`/api/ai`)

`POST /assistant`, `/summarize`, `/draft-email`, `/score-lead`, `/classify`,
`/suggest-task`; audit trail at `GET /actions`; human confirm via
`POST /actions/{id}/apply` and `/actions/{id}/reject`.

Every call is recorded as an `AgentAction`. Write proposals (e.g. `suggest-task`)
are stored as `suggested` and only mutate CRM data after an explicit
`apply`. Set `AI_PROVIDER=anthropic` (or `openai`) and the matching key to use a
real model; the default `mock` provider returns clearly-labelled placeholder text
so the product is fully usable without a key.

## Notes

- The Django project package is `offsideventures` (`DJANGO_SETTINGS_MODULE=offsideventures.settings`).
  If you deploy with gunicorn, the app is `offsideventures.wsgi:application`.
- `requirements.txt` still carries some dependencies from the previous app; they are
  harmless but can be pruned later.
