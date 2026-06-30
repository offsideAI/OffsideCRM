"""Ninja router mounted at /api/ai. Every call is recorded as an AgentAction.

Read-only AI (assistant, summarize, score, classify, draft) is logged as
``applied``. Write proposals (suggest-task) are logged as ``suggested`` with a
``proposed_payload`` and require an explicit human confirm via
``/actions/{id}/apply`` before any CRM record is created.
"""
from typing import List, Optional

from ninja import Router, Schema

from ..models import AgentAction, Company, Contact, Deal, Note, Task
from ..schemas import AgentActionOut, Message
from . import service
from .prompts import SYSTEM_COPILOT, build_context

router = Router()

TARGET_MODELS = {"company": Company, "contact": Contact, "deal": Deal}


def _resolve_target(target_type: Optional[str], target_id: Optional[int]):
    model = TARGET_MODELS.get((target_type or "").lower())
    if not model or not target_id:
        return None
    return model.objects.filter(pk=target_id).first()


def _actor(request):
    user = getattr(request, "auth", None)
    return user if user is not None and user.is_authenticated else None


def _log(request, action_type, *, status, prompt="", result=None, proposed=None,
         target_type="", target_id=None):
    return AgentAction.objects.create(
        action_type=action_type,
        status=status,
        prompt=prompt,
        result=result or {},
        proposed_payload=proposed or {},
        target_type=target_type or "",
        target_id=target_id,
        model=service.active_model(),
        actor=_actor(request),
    )


def _split_email(text: str):
    subject = ""
    body = text.strip()
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.lower().startswith("subject:"):
            subject = line.split(":", 1)[1].strip()
            body = "\n".join(lines[i + 1:]).strip()
            break
    return (subject or "Quick follow-up"), body


def _lead_score(obj, target_type: str) -> int:
    score = 40
    if target_type == "contact":
        score += 20 if obj.email else 0
        score += 10 if obj.phone else 0
        score += 15 if obj.company_id else 0
        score += 15 if obj.status in ("active", "customer") else 0
    else:  # company
        score += 15 if obj.email else 0
        score += 10 if obj.domain else 0
        score += 20 if obj.status in ("active", "customer") else 0
        score += 15 if obj.size in ("201-1000", "1000+") else 0
    return max(0, min(100, score))


# --------------------------------------------------------------------------- #
# Request / response schemas
# --------------------------------------------------------------------------- #
class AssistantIn(Schema):
    message: str
    target_type: Optional[str] = None
    target_id: Optional[int] = None


class TargetIn(Schema):
    target_type: str
    target_id: int


class DraftEmailIn(Schema):
    instructions: str = ""
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None


class ScoreIn(Schema):
    contact_id: Optional[int] = None
    company_id: Optional[int] = None


class ClassifyIn(Schema):
    text: str


class SuggestTaskIn(Schema):
    target_type: str
    target_id: int
    instructions: str = ""


class AssistantOut(Schema):
    reply: str
    agent_action_id: int
    provider: str
    model: str


class TextOut(Schema):
    text: str
    agent_action_id: int


class DraftEmailOut(Schema):
    subject: str
    body: str
    agent_action_id: int


class ScoreOut(Schema):
    score: int
    rationale: str
    agent_action_id: int


class ClassifyOut(Schema):
    category: str
    rationale: str
    agent_action_id: int


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #
@router.post("/assistant", response=AssistantOut)
def assistant(request, payload: AssistantIn):
    obj = _resolve_target(payload.target_type, payload.target_id)
    context = build_context(payload.target_type or "", obj) if obj else ""
    context_block = f"CRM context:\n{context}\n\n" if context else ""
    user_prompt = f"{context_block}User question:\n{payload.message}"
    reply = service.chat(SYSTEM_COPILOT, user_prompt, max_tokens=1024)
    action = _log(
        request, "assistant", status=AgentAction.APPLIED, prompt=payload.message,
        result={"reply": reply}, target_type=payload.target_type or "", target_id=payload.target_id,
    )
    return {
        "reply": reply,
        "agent_action_id": action.id,
        "provider": service.provider(),
        "model": service.active_model(),
    }


@router.post("/summarize", response={200: TextOut, 404: Message})
def summarize(request, payload: TargetIn):
    obj = _resolve_target(payload.target_type, payload.target_id)
    if not obj:
        return 404, {"message": "Target not found"}
    context = build_context(payload.target_type, obj)
    prompt = (
        f"Summarize this {payload.target_type} for a sales rep in 4-6 sentences. "
        "Cover current status, the opportunity, any risks, and the recommended next step.\n\n"
        f"{context}"
    )
    text = service.chat(SYSTEM_COPILOT, prompt, max_tokens=600)
    action = _log(
        request, "summarize_record", status=AgentAction.APPLIED,
        result={"summary": text}, target_type=payload.target_type, target_id=payload.target_id,
    )
    return 200, {"text": text, "agent_action_id": action.id}


@router.post("/draft-email", response=DraftEmailOut)
def draft_email(request, payload: DraftEmailIn):
    parts = []
    if payload.contact_id:
        contact = Contact.objects.filter(pk=payload.contact_id).first()
        if contact:
            parts.append(build_context("contact", contact))
    if payload.deal_id:
        deal = Deal.objects.filter(pk=payload.deal_id).first()
        if deal:
            parts.append(build_context("deal", deal))
    context = "\n\n".join(parts)
    context_block = f"CRM context:\n{context}\n\n" if context else ""
    instructions = payload.instructions or "Write a friendly, concise follow-up."
    prompt = (
        "Draft a short, professional outreach email.\n"
        f"Instructions: {instructions}\n\n"
        f"{context_block}"
        "Return the email starting with a 'Subject:' line, then a blank line, then the body."
    )
    text = service.chat(SYSTEM_COPILOT, prompt, max_tokens=700)
    subject, body = _split_email(text)
    action = _log(
        request, "draft_email", status=AgentAction.APPLIED, prompt=payload.instructions,
        result={"subject": subject, "body": body},
        target_type="contact" if payload.contact_id else ("deal" if payload.deal_id else ""),
        target_id=payload.contact_id or payload.deal_id,
    )
    return {"subject": subject, "body": body, "agent_action_id": action.id}


@router.post("/score-lead", response={200: ScoreOut, 404: Message})
def score_lead(request, payload: ScoreIn):
    obj, target_type, target_id = None, "", None
    if payload.contact_id:
        obj, target_type, target_id = (
            Contact.objects.filter(pk=payload.contact_id).first(), "contact", payload.contact_id,
        )
    elif payload.company_id:
        obj, target_type, target_id = (
            Company.objects.filter(pk=payload.company_id).first(), "company", payload.company_id,
        )
    if not obj:
        return 404, {"message": "Provide a valid contact_id or company_id"}
    score = _lead_score(obj, target_type)
    context = build_context(target_type, obj)
    prompt = (
        f"This lead scored {score} out of 100. In 2-3 sentences, explain the score "
        "and recommend the single best next action.\n\n"
        f"{context}"
    )
    rationale = service.chat(SYSTEM_COPILOT, prompt, max_tokens=300)
    action = _log(
        request, "score_lead", status=AgentAction.APPLIED,
        result={"score": score, "rationale": rationale}, target_type=target_type, target_id=target_id,
    )
    return 200, {"score": score, "rationale": rationale, "agent_action_id": action.id}


@router.post("/classify", response=ClassifyOut)
def classify(request, payload: ClassifyIn):
    categories = "Hot Lead, Warm Lead, Cold Lead, Support Request, Partnership, Not a Fit"
    prompt = (
        f"Classify the following inbound message into exactly one of these categories: {categories}. "
        "Reply with the category on the first line, then a one-sentence reason on the next line.\n\n"
        f"Message:\n{payload.text}"
    )
    text = service.chat(SYSTEM_COPILOT, prompt, max_tokens=200)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    category = lines[0] if lines else "Uncategorized"
    rationale = " ".join(lines[1:]) if len(lines) > 1 else text.strip()
    action = _log(
        request, "classify", status=AgentAction.APPLIED, prompt=payload.text,
        result={"category": category, "rationale": rationale},
    )
    return {"category": category, "rationale": rationale, "agent_action_id": action.id}


@router.post("/suggest-task", response={200: AgentActionOut, 404: Message})
def suggest_task(request, payload: SuggestTaskIn):
    obj = _resolve_target(payload.target_type, payload.target_id)
    if not obj:
        return 404, {"message": "Target not found"}
    context = build_context(payload.target_type, obj)
    instructions = payload.instructions or "Propose the single most valuable next task for this record."
    prompt = (
        f"{instructions}\n"
        "Return a concise task title on the first line and a one-line description on the second line.\n\n"
        f"{context}"
    )
    text = service.chat(SYSTEM_COPILOT, prompt, max_tokens=200)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = (lines[0] if lines else "Follow up")[:255]
    description = lines[1] if len(lines) > 1 else ""
    proposed = {
        "title": title,
        "description": description,
        "priority": "medium",
        f"{payload.target_type}_id": payload.target_id,
    }
    action = _log(
        request, "create_task", status=AgentAction.SUGGESTED, prompt=instructions,
        proposed=proposed, target_type=payload.target_type, target_id=payload.target_id,
    )
    return 200, action


# ---- Agent action audit trail + human confirmation ----
@router.get("/actions", response=List[AgentActionOut])
def list_actions(request, status: Optional[str] = None, limit: int = 50):
    qs = AgentAction.objects.all()
    if status:
        qs = qs.filter(status=status)
    return list(qs[: max(1, min(limit, 200))])


@router.post("/actions/{action_id}/apply", response={200: AgentActionOut, 400: Message, 404: Message})
def apply_action(request, action_id: int):
    action = AgentAction.objects.filter(pk=action_id).first()
    if not action:
        return 404, {"message": "Not found"}
    if action.status != AgentAction.SUGGESTED:
        return 400, {"message": f"Action is '{action.status}', not 'suggested'"}
    payload = action.proposed_payload or {}
    if action.action_type == "create_task":
        Task.objects.create(
            title=payload.get("title", "Follow up"),
            description=payload.get("description", ""),
            priority=payload.get("priority", "medium"),
            company_id=payload.get("company_id"),
            contact_id=payload.get("contact_id"),
            deal_id=payload.get("deal_id"),
            assignee=_actor(request),
        )
    elif action.action_type == "create_note":
        Note.objects.create(
            body=payload.get("body", ""),
            author=_actor(request),
            company_id=payload.get("company_id"),
            contact_id=payload.get("contact_id"),
            deal_id=payload.get("deal_id"),
        )
    else:
        return 400, {"message": f"Cannot apply action type '{action.action_type}'"}
    action.status = AgentAction.APPLIED
    action.save(update_fields=["status", "updated_at"])
    return 200, action


@router.post("/actions/{action_id}/reject", response={200: AgentActionOut, 404: Message})
def reject_action(request, action_id: int):
    action = AgentAction.objects.filter(pk=action_id).first()
    if not action:
        return 404, {"message": "Not found"}
    action.status = AgentAction.REJECTED
    action.save(update_fields=["status", "updated_at"])
    return 200, action
