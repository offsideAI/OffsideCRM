import type { RequestHandler } from '@sveltejs/kit';
import { logout } from '$lib/server/auth';

export const POST: RequestHandler = async (event) => {
  await logout(event);
  return new Response(null, { status: 204 });
};
