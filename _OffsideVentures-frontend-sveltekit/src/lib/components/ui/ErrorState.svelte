<script lang="ts">
  import { TriangleAlert } from 'lucide-svelte';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  interface Props {
    title?: string;
    description?: string;
    children?: Snippet; // optional retry action
    class?: string;
  }

  let {
    title = 'Something went wrong',
    description,
    children,
    class: className
  }: Props = $props();
</script>

<div
  class={cn(
    'flex flex-col items-center justify-center rounded-xl border border-danger/25 bg-danger/5 px-6 py-12 text-center',
    className
  )}
>
  <div
    class="mb-3 flex h-11 w-11 items-center justify-center rounded-full border border-danger/25 bg-danger/10 text-danger"
  >
    <TriangleAlert class="h-5 w-5" />
  </div>
  <p class="text-sm font-medium text-text">{title}</p>
  {#if description}
    <p class="mt-1 max-w-sm text-sm text-text-subtle">{description}</p>
  {/if}
  {#if children}
    <div class="mt-4">{@render children()}</div>
  {/if}
</div>
