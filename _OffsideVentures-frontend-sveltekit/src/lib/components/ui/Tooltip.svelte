<script lang="ts">
  import { Tooltip } from 'bits-ui';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  interface Props {
    text: string;
    side?: 'top' | 'right' | 'bottom' | 'left';
    trigger: Snippet;
    class?: string;
  }

  let { text, side = 'top', trigger, class: className }: Props = $props();
</script>

<Tooltip.Provider delayDuration={200}>
  <Tooltip.Root>
    <Tooltip.Trigger class="inline-flex outline-none">
      {@render trigger()}
    </Tooltip.Trigger>
    <Tooltip.Portal>
      <Tooltip.Content
        {side}
        sideOffset={6}
        class={cn(
          'z-50 rounded-md border border-border bg-surface-2 px-2 py-1 text-xs text-text shadow-lg',
          className
        )}
      >
        {text}
      </Tooltip.Content>
    </Tooltip.Portal>
  </Tooltip.Root>
</Tooltip.Provider>
