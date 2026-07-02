<script lang="ts">
  import { Dialog } from 'bits-ui';
  import { X } from 'lucide-svelte';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  // A side slide-over, built on the dialog primitive for focus management.
  interface Props {
    open?: boolean;
    title?: string;
    side?: 'right' | 'left';
    class?: string;
    children?: Snippet;
    footer?: Snippet;
  }

  let {
    open = $bindable(false),
    title = '',
    side = 'right',
    class: className,
    children,
    footer
  }: Props = $props();
</script>

<Dialog.Root bind:open>
  <Dialog.Portal>
    <Dialog.Overlay class="fixed inset-0 z-50 bg-black/60" />
    <Dialog.Content
      class={cn(
        'fixed inset-y-0 z-50 flex w-full max-w-md flex-col bg-surface-1 shadow-2xl focus:outline-none',
        side === 'right' ? 'right-0 border-l border-border' : 'left-0 border-r border-border',
        className
      )}
    >
      <div class="flex items-center justify-between border-b border-border px-5 py-4">
        <Dialog.Title class="text-sm font-semibold text-text">{title}</Dialog.Title>
        <Dialog.Close
          class="rounded-md p-1 text-text-subtle transition-colors hover:bg-surface-2 hover:text-text"
        >
          <X class="h-4 w-4" />
        </Dialog.Close>
      </div>
      <div class="flex-1 overflow-y-auto p-5">
        {@render children?.()}
      </div>
      {#if footer}
        <div class="border-t border-border px-5 py-4">
          {@render footer()}
        </div>
      {/if}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
