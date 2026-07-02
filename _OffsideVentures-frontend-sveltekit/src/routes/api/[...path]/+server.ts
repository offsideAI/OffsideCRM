import { json, type RequestHandler } from '@sveltejs/kit';
import { apiRequest } from '$lib/server/api';

// BFF proxy: the browser calls same-origin /api/*, this forwards to Django with
// the JWT from the httpOnly cookie. The Django origin stays server-side.
const handle: RequestHandler = async (event) => {
  const path = event.params.path ?? '';
  const fullPath = path + event.url.search;
  const method = event.request.method;
  const sendsBody = method !== 'GET' && method !== 'HEAD' && method !== 'DELETE';
  const body = sendsBody ? await event.request.text() : undefined;

  const { status, data } = await apiRequest(event, method, fullPath, body);
  if (status === 204 || data === null) return new Response(null, { status });
  return json(data, { status });
};

export const GET = handle;
export const POST = handle;
export const PATCH = handle;
export const PUT = handle;
export const DELETE = handle;
