"""Django Ninja request/response schemas for the OffsideVentures CRM API.

Output schemas resolve plain model attributes by field name (Ninja convention);
`*_id` fields pull the FK id, and a few `resolve_*` helpers add denormalized
labels (company name, stage name, …) that the frontend renders without an extra
round-trip. Input schemas are split into create (`*In`) and partial-update
(`*Patch`, all-optional) variants.
"""
from datetime import date, datetime
from typing import List, Optional

from ninja import Schema


# --------------------------------------------------------------------------- #
# Shared
# --------------------------------------------------------------------------- #
class Message(Schema):
    message: str


class UserOut(Schema):
    id: int
    email: str
    first_name: str = ""
    last_name: str = ""


# --------------------------------------------------------------------------- #
# Company
# --------------------------------------------------------------------------- #
class CompanyOut(Schema):
    id: int
    name: str
    domain: str
    industry: str
    size: str
    status: str
    description: str
    phone: str
    email: str
    linkedin_url: str
    logo_url: str
    annual_revenue: Optional[float] = None
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    owner_id: Optional[int] = None
    contacts_count: int = 0
    deals_count: int = 0
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def resolve_contacts_count(obj):
        val = getattr(obj, "contacts_count", None)
        return val if val is not None else obj.contacts.count()

    @staticmethod
    def resolve_deals_count(obj):
        val = getattr(obj, "deals_count", None)
        return val if val is not None else obj.deals.count()


class CompanyIn(Schema):
    name: str
    domain: str = ""
    industry: str = ""
    size: str = ""
    status: str = "prospect"
    description: str = ""
    phone: str = ""
    email: str = ""
    linkedin_url: str = ""
    logo_url: str = ""
    annual_revenue: Optional[float] = None
    street: str = ""
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = ""
    owner_id: Optional[int] = None


class CompanyPatch(Schema):
    name: Optional[str] = None
    domain: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    logo_url: Optional[str] = None
    annual_revenue: Optional[float] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    owner_id: Optional[int] = None


# --------------------------------------------------------------------------- #
# Contact
# --------------------------------------------------------------------------- #
class ContactOut(Schema):
    id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    phone: str
    job_title: str
    status: str
    linkedin_url: str
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def resolve_full_name(obj):
        return obj.full_name

    @staticmethod
    def resolve_company_name(obj):
        return obj.company.name if obj.company_id else None


class ContactIn(Schema):
    first_name: str
    last_name: str = ""
    email: str = ""
    phone: str = ""
    job_title: str = ""
    status: str = "lead"
    linkedin_url: str = ""
    company_id: Optional[int] = None
    owner_id: Optional[int] = None


class ContactPatch(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    status: Optional[str] = None
    linkedin_url: Optional[str] = None
    company_id: Optional[int] = None
    owner_id: Optional[int] = None


# --------------------------------------------------------------------------- #
# Pipeline & Stage
# --------------------------------------------------------------------------- #
class StageOut(Schema):
    id: int
    pipeline_id: int
    name: str
    order: int
    probability: int
    is_won: bool
    is_lost: bool


class StageIn(Schema):
    pipeline_id: int
    name: str
    order: int = 0
    probability: int = 0
    is_won: bool = False
    is_lost: bool = False


class StagePatch(Schema):
    name: Optional[str] = None
    order: Optional[int] = None
    probability: Optional[int] = None
    is_won: Optional[bool] = None
    is_lost: Optional[bool] = None


class PipelineOut(Schema):
    id: int
    name: str
    is_default: bool
    stages: List[StageOut] = []


class PipelineIn(Schema):
    name: str
    is_default: bool = False


# --------------------------------------------------------------------------- #
# Deal
# --------------------------------------------------------------------------- #
class DealOut(Schema):
    id: int
    name: str
    company_id: Optional[int] = None
    company_name: Optional[str] = None
    primary_contact_id: Optional[int] = None
    primary_contact_name: Optional[str] = None
    pipeline_id: int
    stage_id: int
    stage_name: Optional[str] = None
    amount: float
    currency: str
    status: str
    close_date: Optional[date] = None
    description: str
    owner_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def resolve_company_name(obj):
        return obj.company.name if obj.company_id else None

    @staticmethod
    def resolve_primary_contact_name(obj):
        return obj.primary_contact.full_name if obj.primary_contact_id else None

    @staticmethod
    def resolve_stage_name(obj):
        return obj.stage.name if obj.stage_id else None


class DealIn(Schema):
    name: str
    pipeline_id: int
    stage_id: int
    company_id: Optional[int] = None
    primary_contact_id: Optional[int] = None
    amount: float = 0
    currency: str = "USD"
    status: str = "open"
    close_date: Optional[date] = None
    description: str = ""
    owner_id: Optional[int] = None


class DealPatch(Schema):
    name: Optional[str] = None
    pipeline_id: Optional[int] = None
    stage_id: Optional[int] = None
    company_id: Optional[int] = None
    primary_contact_id: Optional[int] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    close_date: Optional[date] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None


# --------------------------------------------------------------------------- #
# Task
# --------------------------------------------------------------------------- #
class TaskOut(Schema):
    id: int
    title: str
    description: str
    status: str
    priority: str
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    assignee_id: Optional[int] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class TaskIn(Schema):
    title: str
    description: str = ""
    status: str = "todo"
    priority: str = "medium"
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None


class TaskPatch(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None


# --------------------------------------------------------------------------- #
# Note
# --------------------------------------------------------------------------- #
class NoteOut(Schema):
    id: int
    body: str
    author_id: Optional[int] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class NoteIn(Schema):
    body: str
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None


# --------------------------------------------------------------------------- #
# Activity (timeline)
# --------------------------------------------------------------------------- #
class ActivityOut(Schema):
    id: int
    type: str
    summary: str
    body: str
    actor_id: Optional[int] = None
    occurred_at: datetime
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    created_at: datetime


class ActivityIn(Schema):
    type: str = "note"
    summary: str
    body: str = ""
    occurred_at: Optional[datetime] = None
    company_id: Optional[int] = None
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None


# --------------------------------------------------------------------------- #
# Agent actions (AI audit trail)
# --------------------------------------------------------------------------- #
class AgentActionOut(Schema):
    id: int
    action_type: str
    status: str
    prompt: str
    result: dict
    proposed_payload: dict
    target_type: str
    target_id: Optional[int] = None
    model: str
    actor_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class AgentActionStatusIn(Schema):
    status: str  # approved | applied | rejected
