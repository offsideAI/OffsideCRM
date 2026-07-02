import { dev } from '$app/environment';
import type { Cookies } from '@sveltejs/kit';

// JWTs live in httpOnly cookies set by the SvelteKit server — the browser never
// sees them, and the Django origin is never exposed client-side.
const ACCESS = 'ov_access';
const REFRESH = 'ov_refresh';

const base = {
  path: '/',
  httpOnly: true,
  sameSite: 'lax' as const,
  secure: !dev
};

export const getAccess = (cookies: Cookies) => cookies.get(ACCESS);
export const getRefresh = (cookies: Cookies) => cookies.get(REFRESH);

export function setAccess(cookies: Cookies, access: string) {
  cookies.set(ACCESS, access, { ...base, maxAge: 60 * 30 }); // 30 min
}

export function setTokens(cookies: Cookies, access: string, refresh: string) {
  setAccess(cookies, access);
  cookies.set(REFRESH, refresh, { ...base, maxAge: 60 * 60 * 24 * 14 }); // 14 days
}

export function clearTokens(cookies: Cookies) {
  cookies.delete(ACCESS, { path: '/' });
  cookies.delete(REFRESH, { path: '/' });
}

/** Minimal event shape the server API/auth helpers need (works for both
 *  endpoint `RequestEvent`s and `load` `ServerLoadEvent`s). */
export type AuthEvent = { cookies: Cookies };
