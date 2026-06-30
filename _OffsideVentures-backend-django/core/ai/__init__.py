"""AI subsystem: provider-agnostic LLM access + Ninja router for /api/ai.

API keys never leave the server — the SvelteKit frontend only ever calls these
Django endpoints, which call the LLM provider on its behalf.
"""
