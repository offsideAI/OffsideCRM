import { fail, redirect } from '@sveltejs/kit';
import { login } from '$lib/server/auth';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async (event) => {
    const data = await event.request.formData();
    const email = String(data.get('email') ?? '').trim();
    const password = String(data.get('password') ?? '');

    if (!email || !password) {
      return fail(400, { error: 'Email and password are required.', email });
    }

    const result = await login(event, email, password);
    if (!result.ok) {
      return fail(401, { error: result.error, email });
    }

    redirect(303, '/app/dashboard');
  }
};
