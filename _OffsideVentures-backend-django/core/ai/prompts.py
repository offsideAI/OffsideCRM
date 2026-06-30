"""System prompts and CRM-record context builders for the AI endpoints."""
from __future__ import annotations

SYSTEM_COPILOT = (
    "You are OffsideVentures Copilot, an AI assistant embedded in a B2B sales CRM. "
    "Be concise, specific, and practical. Ground every statement in the CRM context "
    "you are given. If information is missing, say so plainly. Never invent contacts, "
    "companies, amounts, or dates."
)


def company_context(company) -> str:
    lines = [
        f"Company: {company.name}",
        f"Status: {company.get_status_display()}",
        f"Industry: {company.industry or '—'}",
        f"Size: {company.size or '—'}",
        f"Domain: {company.domain or '—'}",
        f"Location: {', '.join(p for p in [company.city, company.country] if p) or '—'}",
    ]
    if company.description:
        lines.append(f"Description: {company.description}")
    contacts = list(company.contacts.all()[:8])
    if contacts:
        lines.append("Contacts: " + "; ".join(f"{c.full_name} ({c.job_title or 'n/a'})" for c in contacts))
    deals = list(company.deals.all()[:8])
    if deals:
        lines.append("Deals: " + "; ".join(f"{d.name} [{d.status}] {d.amount} {d.currency}" for d in deals))
    return "\n".join(lines)


def contact_context(contact) -> str:
    lines = [
        f"Contact: {contact.full_name}",
        f"Title: {contact.job_title or '—'}",
        f"Email: {contact.email or '—'}",
        f"Status: {contact.get_status_display()}",
        f"Company: {contact.company.name if contact.company_id else '—'}",
    ]
    notes = list(contact.notes.all()[:5])
    if notes:
        lines.append("Recent notes: " + " | ".join(n.body[:160] for n in notes))
    return "\n".join(lines)


def deal_context(deal) -> str:
    lines = [
        f"Deal: {deal.name}",
        f"Stage: {deal.stage.name if deal.stage_id else '—'}",
        f"Status: {deal.get_status_display()}",
        f"Amount: {deal.amount} {deal.currency}",
        f"Close date: {deal.close_date or '—'}",
        f"Company: {deal.company.name if deal.company_id else '—'}",
        f"Primary contact: {deal.primary_contact.full_name if deal.primary_contact_id else '—'}",
    ]
    if deal.description:
        lines.append(f"Description: {deal.description}")
    return "\n".join(lines)


def build_context(target_type: str, obj) -> str:
    if obj is None:
        return ""
    builder = {
        "company": company_context,
        "contact": contact_context,
        "deal": deal_context,
    }.get(target_type)
    return builder(obj) if builder else ""
