"""Provider-agnostic LLM access. API keys live in the Django environment only.

Set ``AI_PROVIDER`` to ``anthropic``, ``openai``, or ``mock`` (default). The mock
provider returns deterministic, clearly-labelled text so the product is fully
functional without any API key — handy for local dev, CI, and demos.
"""
from __future__ import annotations

from django.conf import settings


class AIConfigError(RuntimeError):
    """Raised when a live provider is selected but misconfigured."""


def provider() -> str:
    return (getattr(settings, "AI_PROVIDER", "mock") or "mock").lower()


def is_live() -> bool:
    return provider() in ("anthropic", "openai")


def active_model() -> str:
    configured = getattr(settings, "AI_MODEL", "") or ""
    if configured:
        return configured
    return {"anthropic": "claude-sonnet-4-6", "openai": "gpt-4o-mini"}.get(provider(), "mock")


def chat(system: str, user: str, *, model: str | None = None, max_tokens: int = 1024) -> str:
    """Single-turn completion. Returns the assistant's text."""
    p = provider()
    if p == "anthropic":
        return _anthropic(system, user, model, max_tokens)
    if p == "openai":
        return _openai(system, user, model, max_tokens)
    return _mock(system, user)


def _anthropic(system, user, model, max_tokens) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise AIConfigError("The 'anthropic' package is not installed.") from exc
    key = getattr(settings, "ANTHROPIC_API_KEY", "")
    if not key:
        raise AIConfigError("ANTHROPIC_API_KEY is not set.")
    client = anthropic.Anthropic(api_key=key)
    resp = client.messages.create(
        model=model or active_model(),
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(getattr(block, "text", "") for block in resp.content)


def _openai(system, user, model, max_tokens) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise AIConfigError("The 'openai' package is not installed.") from exc
    key = getattr(settings, "OPENAI_API_KEY", "")
    if not key:
        raise AIConfigError("OPENAI_API_KEY is not set.")
    client = OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model=model or active_model(),
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content or ""


def _mock(system, user) -> str:
    # Deterministic and clearly labelled so it's never mistaken for a real model.
    first_line = ""
    for line in user.strip().splitlines():
        if line.strip():
            first_line = line.strip()[:180]
            break
    return (
        "[mock-ai] No live AI provider is configured (AI_PROVIDER=mock), so this is "
        "a placeholder response that keeps the product fully usable. "
        f'Prompt received: "{first_line}".'
    )
