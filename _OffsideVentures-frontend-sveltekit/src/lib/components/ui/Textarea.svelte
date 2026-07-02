<script lang="ts">
  import type { HTMLTextareaAttributes } from 'svelte/elements';
  import { cn } from '$lib/utils/cn';

  interface Props extends HTMLTextareaAttributes {
    value?: string;
  }

  let { class: className, value = $bindable(''), ...rest }: Props = $props();
</script>

<textarea
  bind:value
  class={cn(
    'min-h-20 w-full rounded-lg border border-border bg-surface-2 px-3 py-2 text-sm text-text outline-none transition-colors placeholder:text-text-subtle focus-visible:border-border-strong focus-visible:ring-2 focus-visible:ring-accent',
    className
  )}
  {...rest}
></textarea>
