<script lang="ts">
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  type Tone = 'neutral' | 'accent' | 'success' | 'warning' | 'danger' | 'info';

  interface Props {
    tone?: Tone;
    class?: string;
    children?: Snippet;
  }

  let { tone = 'neutral', class: className, children }: Props = $props();

  const tones: Record<Tone, string> = {
    neutral: 'border-border bg-surface-2 text-text-muted',
    accent: 'border-accent/25 bg-accent/10 text-accent',
    success: 'border-success/25 bg-success/10 text-success',
    warning: 'border-warning/25 bg-warning/10 text-warning',
    danger: 'border-danger/25 bg-danger/10 text-danger',
    info: 'border-info/25 bg-info/10 text-info'
  };
</script>

<span
  class={cn(
    'inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-xs font-medium',
    tones[tone],
    className
  )}
>
  {@render children?.()}
</span>
