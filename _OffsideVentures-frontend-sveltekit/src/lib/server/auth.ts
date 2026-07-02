import { currentUserSchema, type CurrentUser } from '$lib/api/schemas';
import { mockUser } from '$lib/mock/data';
import { apiRequest } from './api';
import { API_BASE_URL, MOCK } from './config';
import { type AuthEvent, clearTokens, getAccess, getRefresh, setTokens } from './cookies';

export type LoginResult = { ok: true } | { ok: false; error: string };

export async function login(event: AuthEvent, email: string, password: string): Promise<LoginResult> {
  if (MOCK) {
    setTokens(event.cookies, 'mock-access', 'mock-refresh');
    return { ok: true };
  }

  const response = await fetch(`${API_BASE_URL}/auth/jwt/create/`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    return {
      ok: false,
      error: response.status === 401 ? 'Invalid email or password.' : 'Sign-in failed. Please try again.'
    };
  }

  const json = (await response.json().catch(() => null)) as { access?: string; refresh?: string } | null;
  if (!json?.access || !json?.refresh) {
    return { ok: false, error: 'Sign-in failed. Please try again.' };
  }
  setTokens(event.cookies, json.access, json.refresh);
  return { ok: true };
}

export async function logout(event: AuthEvent): Promise<void> {
  if (!MOCK) {
    const refresh = getRefresh(event.cookies);
    const access = getAccess(event.cookies);
    if (refresh) {
      // Best-effort token blacklist; clear cookies regardless of the outcome.
      await fetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          ...(access ? { authorization: `Bearer ${access}` } : {})
        },
        body: JSON.stringify({ refresh })
      }).catch(() => undefined);
    }
  }
  clearTokens(event.cookies);
}

export async function getCurrentUser(event: AuthEvent): Promise<CurrentUser | null> {
  if (MOCK) return mockUser;
  if (!getAccess(event.cookies)) return null;
  const { status, data } = await apiRequest(event, 'GET', 'me');
  if (status !== 200) return null;
  const parsed = currentUserSchema.safeParse(data);
  return parsed.success ? parsed.data : null;
}
