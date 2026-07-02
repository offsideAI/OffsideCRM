<script lang="ts">
  import type { Snippet } from 'svelte';
  import type { HTMLLabelAttributes } from 'svelte/elements';
  import { cn } from '$lib/utils/cn';

  interface Props extends HTMLLabelAttributes {
    children?: Snippet;
  }

  let { class: className, children, ...rest }: Props = $props();
</script>

<label class={cn('text-sm font-medium text-text', className)} {...rest}>
  {@render children?.()}
</label>
