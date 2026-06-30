"""OffsideVentures CRM API (Django Ninja).

JWT-authenticated CRUD for the CRM objects plus a mounted AI router at /api/ai.
Auto OpenAPI lives at /api/openapi.json, dark Swagger UI at /api/docs.
"""
from typing import List, Optional

from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Router
from ninja.openapi.docs import DocsBase
from ninja.pagination import LimitOffsetPagination, paginate

from .ai.api import router as ai_router
from .ai.service import AIConfigError
from .authentication import JWTAuth
from .models import Activity, Company, Contact, Deal, Note, Pipeline, Stage, Task
from .schemas import (
    ActivityIn,
    ActivityOut,
    CompanyIn,
    CompanyOut,
    CompanyPatch,
    ContactIn,
    ContactOut,
    ContactPatch,
    DealIn,
    DealOut,
    DealPatch,
    Message,
    NoteIn,
    NoteOut,
    PipelineIn,
    PipelineOut,
    StageIn,
    StageOut,
    StagePatch,
    TaskIn,
    TaskOut,
    TaskPatch,
    UserOut,
)

# A restrained dark Swagger theme matching the OffsideVentures palette
# (monochrome graphite surfaces + a single signal-red accent).
DARK_CSS = """
:root { --bg:#0B0C0E; --bg2:#141518; --bg3:#1C1F23; --bd:#262A2F; --tx:#E8EAEC; --mut:#9AA0A7; --ac:#E5484D; }
body, .swagger-ui { background:var(--bg) !important; color:var(--tx) !important; }
.swagger-ui .topbar { display:none; }
.swagger-ui .info .title, .swagger-ui .opblock-tag, .swagger-ui .info { color:var(--tx) !important; }
.swagger-ui .info .description, .swagger-ui .info p { color:var(--mut) !important; }
.swagger-ui .scheme-container, .swagger-ui .opblock, .swagger-ui section.models { background:var(--bg2) !important; border:1px solid var(--bd) !important; border-radius:10px !important; box-shadow:none !important; }
.swagger-ui .opblock .opblock-summary-method { background:var(--bg3) !important; border-radius:6px !important; }
.swagger-ui .opblock.opblock-post { border-color:var(--ac) !important; }
.swagger-ui .opblock.opblock-post .opblock-summary-method { background:var(--ac) !important; }
.swagger-ui .opblock-summary-path, .swagger-ui .opblock-summary-description, .swagger-ui table thead tr th, .swagger-ui .parameter__name { color:var(--tx) !important; }
.swagger-ui input, .swagger-ui textarea, .swagger-ui select { background:var(--bg3) !important; color:var(--tx) !important; border:1px solid var(--bd) !important; border-radius:6px !important; }
.swagger-ui .btn { border-radius:6px !important; }
.swagger-ui .btn.execute, .swagger-ui .btn.authorize { background:var(--ac) !important; border-color:var(--ac) !important; color:#fff !important; }
.swagger-ui .opblock-body pre, .swagger-ui .microlight { background:var(--bg) !important; color:var(--tx) !important; border:1px solid var(--bd); border-radius:6px; }
"""


class DarkSwaggerDocs(DocsBase):
    def render_page(self, request, api, **kwargs):
        html = f"""<!DOCTYPE html>
<html><head><title>OffsideVentures API</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
<style>{DARK_CSS}</style></head>
<body><div id="swagger-ui"></div>
<script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>window.onload = function() {{ SwaggerUIBundle({{
  url: "{api.root_path}/openapi.json", dom_id: '#swagger-ui',
  presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
  layout: "BaseLayout", persistAuthorization: true, docExpansion: "list" }}); }};</script>
</body></html>"""
        return HttpResponse(html)


api = NinjaAPI(
    title="OffsideVentures API",
    version="1.0.0",
    description="Agentic-AI-first CRM API.",
    csrf=False,
    auth=JWTAuth(),
    docs=DarkSwaggerDocs(),
)


@api.exception_handler(AIConfigError)
def on_ai_config_error(request, exc):
    return api.create_response(request, {"message": f"AI is not configured: {exc}"}, status=503)


def apply_patch(obj, payload):
    """Apply only the fields the client actually sent (PATCH semantics)."""
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    obj.save()
    return obj


def default_owner(request, data: dict, field: str = "owner_id"):
    """Default record ownership to the calling user when not specified."""
    if data.get(field) is None:
        user = getattr(request, "auth", None)
        if user is not None and user.is_authenticated:
            data[field] = user.id
    return data


# --------------------------------------------------------------------------- #
# Current user
# --------------------------------------------------------------------------- #
@api.get("/me", response=UserOut)
def me(request):
    return request.auth


# --------------------------------------------------------------------------- #
# Companies
# --------------------------------------------------------------------------- #
companies = Router()


@companies.get("/", response=List[CompanyOut])
@paginate(LimitOffsetPagination)
def list_companies(request, search: Optional[str] = None, status: Optional[str] = None,
                   ordering: Optional[str] = None):
    qs = Company.objects.annotate(
        contacts_count=Count("contacts", distinct=True),
        deals_count=Count("deals", distinct=True),
    )
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(domain__icontains=search) | Q(email__icontains=search))
    if status:
        qs = qs.filter(status=status)
    if ordering:
        qs = qs.order_by(ordering)
    return qs


@companies.post("/", response={201: CompanyOut})
def create_company(request, payload: CompanyIn):
    data = default_owner(request, payload.dict())
    return 201, Company.objects.create(**data)


@companies.get("/{company_id}", response={200: CompanyOut, 404: Message})
def get_company(request, company_id: int):
    obj = Company.objects.filter(pk=company_id).first()
    return (200, obj) if obj else (404, {"message": "Company not found"})


@companies.patch("/{company_id}", response={200: CompanyOut, 404: Message})
def update_company(request, company_id: int, payload: CompanyPatch):
    return 200, apply_patch(get_object_or_404(Company, pk=company_id), payload)


@companies.delete("/{company_id}", response={204: None})
def delete_company(request, company_id: int):
    get_object_or_404(Company, pk=company_id).delete()
    return 204, None


# --------------------------------------------------------------------------- #
# Contacts
# --------------------------------------------------------------------------- #
contacts = Router()


@contacts.get("/", response=List[ContactOut])
@paginate(LimitOffsetPagination)
def list_contacts(request, search: Optional[str] = None, status: Optional[str] = None,
                  company_id: Optional[int] = None, ordering: Optional[str] = None):
    qs = Contact.objects.select_related("company")
    if search:
        qs = qs.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search)
        )
    if status:
        qs = qs.filter(status=status)
    if company_id:
        qs = qs.filter(company_id=company_id)
    if ordering:
        qs = qs.order_by(ordering)
    return qs


@contacts.post("/", response={201: ContactOut})
def create_contact(request, payload: ContactIn):
    data = default_owner(request, payload.dict())
    return 201, Contact.objects.create(**data)


@contacts.get("/{contact_id}", response={200: ContactOut, 404: Message})
def get_contact(request, contact_id: int):
    obj = Contact.objects.select_related("company").filter(pk=contact_id).first()
    return (200, obj) if obj else (404, {"message": "Contact not found"})


@contacts.patch("/{contact_id}", response={200: ContactOut, 404: Message})
def update_contact(request, contact_id: int, payload: ContactPatch):
    return 200, apply_patch(get_object_or_404(Contact, pk=contact_id), payload)


@contacts.delete("/{contact_id}", response={204: None})
def delete_contact(request, contact_id: int):
    get_object_or_404(Contact, pk=contact_id).delete()
    return 204, None


# --------------------------------------------------------------------------- #
# Pipelines & stages
# --------------------------------------------------------------------------- #
pipelines = Router()


@pipelines.get("/", response=List[PipelineOut])
def list_pipelines(request):
    return list(Pipeline.objects.prefetch_related("stages"))


@pipelines.post("/", response={201: PipelineOut})
def create_pipeline(request, payload: PipelineIn):
    return 201, Pipeline.objects.create(**payload.dict())


@pipelines.post("/stages", response={201: StageOut})
def create_stage(request, payload: StageIn):
    return 201, Stage.objects.create(**payload.dict())


@pipelines.patch("/stages/{stage_id}", response={200: StageOut, 404: Message})
def update_stage(request, stage_id: int, payload: StagePatch):
    return 200, apply_patch(get_object_or_404(Stage, pk=stage_id), payload)


@pipelines.delete("/stages/{stage_id}", response={204: None})
def delete_stage(request, stage_id: int):
    get_object_or_404(Stage, pk=stage_id).delete()
    return 204, None


# --------------------------------------------------------------------------- #
# Deals
# --------------------------------------------------------------------------- #
deals = Router()


@deals.get("/", response=List[DealOut])
@paginate(LimitOffsetPagination)
def list_deals(request, search: Optional[str] = None, status: Optional[str] = None,
               pipeline_id: Optional[int] = None, stage_id: Optional[int] = None,
               company_id: Optional[int] = None, ordering: Optional[str] = None):
    qs = Deal.objects.select_related("company", "primary_contact", "stage")
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(company__name__icontains=search))
    if status:
        qs = qs.filter(status=status)
    if pipeline_id:
        qs = qs.filter(pipeline_id=pipeline_id)
    if stage_id:
        qs = qs.filter(stage_id=stage_id)
    if company_id:
        qs = qs.filter(company_id=company_id)
    if ordering:
        qs = qs.order_by(ordering)
    return qs


@deals.post("/", response={201: DealOut})
def create_deal(request, payload: DealIn):
    data = default_owner(request, payload.dict())
    return 201, Deal.objects.create(**data)


@deals.get("/{deal_id}", response={200: DealOut, 404: Message})
def get_deal(request, deal_id: int):
    obj = Deal.objects.select_related("company", "primary_contact", "stage").filter(pk=deal_id).first()
    return (200, obj) if obj else (404, {"message": "Deal not found"})


@deals.patch("/{deal_id}", response={200: DealOut, 404: Message})
def update_deal(request, deal_id: int, payload: DealPatch):
    return 200, apply_patch(get_object_or_404(Deal, pk=deal_id), payload)


@deals.delete("/{deal_id}", response={204: None})
def delete_deal(request, deal_id: int):
    get_object_or_404(Deal, pk=deal_id).delete()
    return 204, None


# --------------------------------------------------------------------------- #
# Tasks
# --------------------------------------------------------------------------- #
tasks = Router()


@tasks.get("/", response=List[TaskOut])
@paginate(LimitOffsetPagination)
def list_tasks(request, status: Optional[str] = None, assignee_id: Optional[int] = None,
               company_id: Optional[int] = None, contact_id: Optional[int] = None,
               deal_id: Optional[int] = None, ordering: Optional[str] = None):
    qs = Task.objects.all()
    for field, value in (
        ("status", status), ("assignee_id", assignee_id), ("company_id", company_id),
        ("contact_id", contact_id), ("deal_id", deal_id),
    ):
        if value is not None:
            qs = qs.filter(**{field: value})
    if ordering:
        qs = qs.order_by(ordering)
    return qs


@tasks.post("/", response={201: TaskOut})
def create_task(request, payload: TaskIn):
    return 201, Task.objects.create(**payload.dict())


@tasks.patch("/{task_id}", response={200: TaskOut, 404: Message})
def update_task(request, task_id: int, payload: TaskPatch):
    return 200, apply_patch(get_object_or_404(Task, pk=task_id), payload)


@tasks.delete("/{task_id}", response={204: None})
def delete_task(request, task_id: int):
    get_object_or_404(Task, pk=task_id).delete()
    return 204, None


# --------------------------------------------------------------------------- #
# Notes
# --------------------------------------------------------------------------- #
notes = Router()


@notes.get("/", response=List[NoteOut])
def list_notes(request, company_id: Optional[int] = None, contact_id: Optional[int] = None,
               deal_id: Optional[int] = None):
    qs = Note.objects.all()
    for field, value in (("company_id", company_id), ("contact_id", contact_id), ("deal_id", deal_id)):
        if value is not None:
            qs = qs.filter(**{field: value})
    return list(qs[:200])


@notes.post("/", response={201: NoteOut})
def create_note(request, payload: NoteIn):
    user = getattr(request, "auth", None)
    return 201, Note.objects.create(
        author=user if user and user.is_authenticated else None, **payload.dict()
    )


@notes.delete("/{note_id}", response={204: None})
def delete_note(request, note_id: int):
    get_object_or_404(Note, pk=note_id).delete()
    return 204, None


# --------------------------------------------------------------------------- #
# Activities (timeline)
# --------------------------------------------------------------------------- #
activities = Router()


@activities.get("/", response=List[ActivityOut])
def list_activities(request, company_id: Optional[int] = None, contact_id: Optional[int] = None,
                    deal_id: Optional[int] = None, limit: int = 100):
    qs = Activity.objects.all()
    for field, value in (("company_id", company_id), ("contact_id", contact_id), ("deal_id", deal_id)):
        if value is not None:
            qs = qs.filter(**{field: value})
    return list(qs[: max(1, min(limit, 200))])


@activities.post("/", response={201: ActivityOut})
def create_activity(request, payload: ActivityIn):
    user = getattr(request, "auth", None)
    data = payload.dict(exclude_unset=True)
    return 201, Activity.objects.create(
        actor=user if user and user.is_authenticated else None, **data
    )


# --------------------------------------------------------------------------- #
# Global search
# --------------------------------------------------------------------------- #
search_router = Router()


@search_router.get("/", response=dict)
def global_search(request, q: str, limit: int = 5):
    limit = max(1, min(limit, 20))
    companies_qs = Company.objects.filter(Q(name__icontains=q) | Q(domain__icontains=q))[:limit]
    contacts_qs = Contact.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
    )[:limit]
    deals_qs = Deal.objects.filter(name__icontains=q)[:limit]
    return {
        "companies": [{"id": c.id, "name": c.name} for c in companies_qs],
        "contacts": [{"id": c.id, "name": c.full_name, "email": c.email} for c in contacts_qs],
        "deals": [{"id": d.id, "name": d.name} for d in deals_qs],
    }


# --------------------------------------------------------------------------- #
# Mount routers
# --------------------------------------------------------------------------- #
api.add_router("/companies", companies)
api.add_router("/contacts", contacts)
api.add_router("/pipelines", pipelines)
api.add_router("/deals", deals)
api.add_router("/tasks", tasks)
api.add_router("/notes", notes)
api.add_router("/activities", activities)
api.add_router("/search", search_router)
api.add_router("/ai", ai_router)
