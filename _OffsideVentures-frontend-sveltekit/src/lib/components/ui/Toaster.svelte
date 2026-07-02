<script lang="ts">
  import { CheckCircle2, Info, TriangleAlert, X } from 'lucide-svelte';
  import { fly } from 'svelte/transition';
  import { toasts, type ToastTone } from '$lib/stores/toast.svelte';
  import { cn } from '$lib/utils/cn';

  const icons = { neutral: Info, success: CheckCircle2, danger: TriangleAlert, info: Info };
  const toneClass: Record<ToastTone, string> = {
    neutral: 'text-text-muted',
    success: 'text-success',
    danger: 'text-danger',
    info: 'text-info'
  };
</script>

<div class="pointer-events-none fixed bottom-4 right-4 z-[100] flex w-80 flex-col gap-2">
  {#each toasts.items as item (item.id)}
    {@const ToastIcon = icons[item.tone]}
    <div
      transition:fly={{ y: 12, duration: 180 }}
      class="pointer-events-auto flex items-start gap-2.5 rounded-lg border border-border bg-surface-1 p-3 shadow-xl"
    >
      <ToastIcon class={cn('mt-0.5 h-4 w-4 shrink-0', toneClass[item.tone])} />
      <p class="flex-1 text-sm text-text">{item.message}</p>
      <button
        onclick={() => toasts.dismiss(item.id)}
        class="rounded p-0.5 text-text-subtle transition-colors hover:text-text"
        aria-label="Dismiss"
      >
        <X class="h-3.5 w-3.5" />
      </button>
    </div>
  {/each}
</div>
