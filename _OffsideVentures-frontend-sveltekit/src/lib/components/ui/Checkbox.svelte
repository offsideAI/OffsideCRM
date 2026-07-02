<script lang="ts">
  import { Check } from 'lucide-svelte';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  interface Props {
    checked?: boolean;
    disabled?: boolean;
    id?: string;
    class?: string;
    children?: Snippet;
  }

  let {
    checked = $bindable(false),
    disabled = false,
    id,
    class: className,
    children
  }: Props = $props();
</script>

<label
  class={cn(
    'inline-flex cursor-pointer select-none items-center gap-2 text-sm',
    disabled && 'cursor-not-allowed opacity-50',
    className
  )}
>
  <span class="relative inline-flex h-4 w-4 items-center justify-center">
    <input
      type="checkbox"
      bind:checked
      {disabled}
      {id}
      class="peer absolute inset-0 cursor-pointer appearance-none rounded border border-border bg-surface-2 transition-colors checked:border-accent checked:bg-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
    />
    <Check class="pointer-events-none h-3 w-3 text-accent-contrast opacity-0 peer-checked:opacity-100" />
  </span>
  {#if children}<span class="text-text">{@render children()}</span>{/if}
</label>
