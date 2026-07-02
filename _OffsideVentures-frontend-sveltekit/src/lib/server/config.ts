import { env } from '$env/dynamic/private';
import { env as publicEnv } from '$env/dynamic/public';

/** Django base URL — server-only; never exposed to the browser. */
export const API_BASE_URL = (env.API_BASE_URL ?? 'http://localhost:8000').replace(/\/+$/, '');

/** Mock-data mode: run the whole app with in-memory fixtures and no backend. */
export const MOCK = (publicEnv.PUBLIC_MOCK ?? '0') === '1';

export interface ApiResult {
  status: number;
  data: unknown;
}
