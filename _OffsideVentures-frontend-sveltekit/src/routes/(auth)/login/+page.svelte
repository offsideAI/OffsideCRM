<script lang="ts">
  import { enhance } from '$app/forms';
  import { ArrowRight } from 'lucide-svelte';
  import { Button } from '$lib/components/ui';
  import type { ActionData } from './$types';

  let { form }: { form: ActionData } = $props();
  let loading = $state(false);

  const inputClass =
    'h-9 w-full rounded-lg border border-border bg-surface-2 px-3 text-sm text-text outline-none transition-colors placeholder:text-text-subtle focus-visible:border-border-strong focus-visible:ring-2 focus-visible:ring-accent';
</script>

<svelte:head><title>Sign in · OffsideVentures</title></svelte:head>

<div class="flex min-h-screen items-center justify-center px-4">
  <div class="w-full max-w-sm">
    <div class="mb-8 flex items-center gap-2.5">
      <span class="grid h-8 w-8 place-items-center rounded-md bg-surface-2 ring-1 ring-border">
        <span class="h-2.5 w-2.5 rounded-[3px] bg-accent"></span>
      </span>
      <span class="text-base font-semibold tracking-tight">OffsideVentures</span>
    </div>

    <h1 class="text-xl font-semibold tracking-tight text-text">Sign in</h1>
    <p class="mt-1 text-sm text-text-muted">Welcome back. Enter your details to continue.</p>

    <form
      method="POST"
      use:enhance={() => {
        loading = true;
        return async ({ update }) => {
          await update();
          loading = false;
        };
      }}
      class="mt-6 space-y-3"
    >
      {#if form?.error}
        <div class="rounded-lg border border-danger/25 bg-danger/10 px-3 py-2 text-sm text-danger">
          {form.error}
        </div>
      {/if}

      <div class="space-y-1.5">
        <label for="email" class="text-sm font-medium text-text">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          autocomplete="email"
          required
          value={form?.email ?? 'demo@offsideventures.com'}
          class={inputClass}
        />
      </div>

      <div class="space-y-1.5">
        <label for="password" class="text-sm font-medium text-text">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          autocomplete="current-password"
          required
          value="offside1234"
          class={inputClass}
        />
      </div>

      <Button type="submit" variant="primary" class="w-full" disabled={loading}>
        {loading ? 'Signing in…' : 'Sign in'}
        <ArrowRight class="h-4 w-4" />
      </Button>
    </form>

    <p class="mt-4 text-center font-mono text-[11px] text-text-subtle">
      Mock mode — any credentials work
    </p>
  </div>
</div>
