<script lang="ts">
  import type { HTMLInputAttributes } from 'svelte/elements';
  import { cn } from '$lib/utils/cn';

  interface Props extends HTMLInputAttributes {
    value?: string;
  }

  let { class: className, value = $bindable(''), ...rest }: Props = $props();
</script>

<input
  bind:value
  class={cn(
    'h-9 w-full rounded-lg border border-border bg-surface-2 px-3 text-sm text-text outline-none transition-colors placeholder:text-text-subtle focus-visible:border-border-strong focus-visible:ring-2 focus-visible:ring-accent',
    className
  )}
  {...rest}
/>
