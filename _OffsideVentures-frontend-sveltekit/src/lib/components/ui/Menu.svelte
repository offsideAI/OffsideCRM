<script lang="ts">
  import { DropdownMenu } from 'bits-ui';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  interface Props {
    trigger: Snippet;
    children: Snippet;
    align?: 'start' | 'center' | 'end';
    triggerClass?: string;
    class?: string;
  }

  let { trigger, children, align = 'end', triggerClass, class: className }: Props = $props();
</script>

<DropdownMenu.Root>
  <DropdownMenu.Trigger class={cn('inline-flex items-center outline-none', triggerClass)}>
    {@render trigger()}
  </DropdownMenu.Trigger>
  <DropdownMenu.Portal>
    <DropdownMenu.Content
      {align}
      sideOffset={6}
      class={cn(
        'z-50 min-w-44 rounded-lg border border-border bg-surface-1 p-1 shadow-xl focus:outline-none',
        className
      )}
    >
      {@render children()}
    </DropdownMenu.Content>
  </DropdownMenu.Portal>
</DropdownMenu.Root>
