<script lang="ts">
  import { Dialog } from 'bits-ui';
  import { X } from 'lucide-svelte';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  interface Props {
    open?: boolean;
    title?: string;
    description?: string;
    class?: string;
    children?: Snippet;
  }

  let { open = $bindable(false), title, description, class: className, children }: Props = $props();
</script>

<Dialog.Root bind:open>
  <Dialog.Portal>
    <Dialog.Overlay class="fixed inset-0 z-50 bg-black/60" />
    <Dialog.Content
      class={cn(
        'fixed left-1/2 top-1/2 z-50 w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-xl border border-border bg-surface-1 p-5 shadow-2xl focus:outline-none',
        className
      )}
    >
      {#if title}
        <div class="mb-4 flex items-start justify-between gap-4">
          <div>
            <Dialog.Title class="text-sm font-semibold text-text">{title}</Dialog.Title>
            {#if description}
              <Dialog.Description class="mt-1 text-sm text-text-muted">
                {description}
              </Dialog.Description>
            {/if}
          </div>
          <Dialog.Close
            class="rounded-md p-1 text-text-subtle transition-colors hover:bg-surface-2 hover:text-text"
          >
            <X class="h-4 w-4" />
          </Dialog.Close>
        </div>
      {/if}
      {@render children?.()}
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
