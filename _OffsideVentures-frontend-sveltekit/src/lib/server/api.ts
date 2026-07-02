import { API_BASE_URL, MOCK, type ApiResult } from './config';
import { type AuthEvent, clearTokens, getAccess, getRefresh, setAccess } from './cookies';
import { mockRequest } from './mock';

// The single server-side gateway to the backend. In MOCK mode it routes to the
// in-memory fixtures; otherwise it forwards to Django with the access token from
// the httpOnly cookie, transparently refreshing on a 401.
export async function apiRequest(
  event: AuthEvent,
  method: string,
  fullPath: string,
  body?: string
): Promise<ApiResult> {
  if (MOCK) {
    const [pathname, search = ''] = fullPath.split('?');
    return mockRequest(method, pathname, new URLSearchParams(search), body);
  }
  return djangoRequest(event, method, fullPath, body, false);
}

async function djangoRequest(
  event: AuthEvent,
  method: string,
  fullPath: string,
  body: string | undefined,
  isRetry: boolean
): Promise<ApiResult> {
  const access = getAccess(event.cookies);
  const sendsBody = method !== 'GET' && method !== 'HEAD' && method !== 'DELETE';
  const response = await fetch(`${API_BASE_URL}/api/${fullPath}`, {
    method,
    headers: {
      'content-type': 'application/json',
      ...(access ? { authorization: `Bearer ${access}` } : {})
    },
    body: sendsBody ? body : undefined
  });

  if (response.status === 401 && !isRetry && (await tryRefresh(event))) {
    return djangoRequest(event, method, fullPath, body, true);
  }

  return { status: response.status, data: await safeJson(response) };
}

async function tryRefresh(event: AuthEvent): Promise<boolean> {
  const refresh = getRefresh(event.cookies);
  if (!refresh) return false;
  const response = await fetch(`${API_BASE_URL}/auth/jwt/refresh/`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ refresh })
  });
  if (!response.ok) {
    clearTokens(event.cookies);
    return false;
  }
  const json = (await response.json().catch(() => null)) as { access?: string } | null;
  if (json?.access) {
    setAccess(event.cookies, json.access);
    return true;
  }
  return false;
}

async function safeJson(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}
