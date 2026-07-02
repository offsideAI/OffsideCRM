<script lang="ts">
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  interface Props {
    title: string;
    description?: string;
    icon?: Snippet;
    children?: Snippet; // optional action(s)
    class?: string;
  }

  let { title, description, icon, children, class: className }: Props = $props();
</script>

<div
  class={cn(
    'flex flex-col items-center justify-center rounded-xl border border-dashed border-border bg-surface-1 px-6 py-12 text-center',
    className
  )}
>
  {#if icon}
    <div
      class="mb-3 flex h-11 w-11 items-center justify-center rounded-full border border-border bg-surface-2 text-text-muted"
    >
      {@render icon()}
    </div>
  {/if}
  <p class="text-sm font-medium text-text">{title}</p>
  {#if description}
    <p class="mt-1 max-w-sm text-sm text-text-subtle">{description}</p>
  {/if}
  {#if children}
    <div class="mt-4">{@render children()}</div>
  {/if}
</div>
