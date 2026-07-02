<script lang="ts">
  import { DropdownMenu } from 'bits-ui';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  interface Props {
    onSelect?: () => void;
    tone?: 'default' | 'danger';
    class?: string;
    children: Snippet;
  }

  let { onSelect, tone = 'default', class: className, children }: Props = $props();
</script>

<DropdownMenu.Item
  {onSelect}
  class={cn(
    'flex cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 text-sm outline-none transition-colors data-[highlighted]:bg-surface-2',
    tone === 'danger' ? 'text-danger' : 'text-text',
    className
  )}
>
  {@render children()}
</DropdownMenu.Item>
