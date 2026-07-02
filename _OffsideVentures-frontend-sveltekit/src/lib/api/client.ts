import type { z } from 'zod';

// Browser-side API client. Calls the same-origin SvelteKit proxy (/api/...),
// which attaches the JWT and forwards to Django — the browser never holds a
// token or sees the Django origin. Responses are validated with Zod.

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request(
  path: string,
  init: RequestInit | undefined,
  fetchFn: typeof fetch
): Promise<unknown> {
  const response = await fetchFn(`/api/${path}`, {
    ...init,
    headers: { 'content-type': 'application/json', ...(init?.headers ?? {}) }
  });
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const message =
      data && typeof data === 'object' && 'message' in data
        ? String((data as { message: unknown }).message)
        : `Request failed (${response.status})`;
    throw new ApiError(response.status, message);
  }
  return data;
}

export async function apiGet<T>(
  path: string,
  schema: z.ZodType<T>,
  fetchFn: typeof fetch = fetch
): Promise<T> {
  return schema.parse(await request(path, undefined, fetchFn));
}

async function apiSend<T>(
  method: string,
  path: string,
  body: unknown,
  schema: z.ZodType<T>,
  fetchFn: typeof fetch
): Promise<T> {
  return schema.parse(await request(path, { method, body: JSON.stringify(body) }, fetchFn));
}

export const apiPost = <T>(path: string, body: unknown, schema: z.ZodType<T>, fetchFn: typeof fetch = fetch) =>
  apiSend('POST', path, body, schema, fetchFn);

export const apiPatch = <T>(path: string, body: unknown, schema: z.ZodType<T>, fetchFn: typeof fetch = fetch) =>
  apiSend('PATCH', path, body, schema, fetchFn);

export async function apiDelete(path: string, fetchFn: typeof fetch = fetch): Promise<void> {
  await request(path, { method: 'DELETE' }, fetchFn);
}
