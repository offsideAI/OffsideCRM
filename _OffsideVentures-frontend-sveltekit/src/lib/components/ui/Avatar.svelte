<script lang="ts">
  import { cn } from '$lib/utils/cn';
  import { initials as toInitials } from '$lib/utils/format';

  interface Props {
    name?: string;
    src?: string | null;
    size?: 'sm' | 'md' | 'lg';
    class?: string;
  }

  let { name = '', src = null, size = 'md', class: className }: Props = $props();

  const sizes = {
    sm: 'h-7 w-7 text-[0.7rem]',
    md: 'h-9 w-9 text-xs',
    lg: 'h-11 w-11 text-sm'
  };
</script>

{#if src}
  <img
    {src}
    alt={name}
    class={cn('rounded-full border border-border object-cover', sizes[size], className)}
  />
{:else}
  <span
    class={cn(
      'inline-flex items-center justify-center rounded-full border border-border bg-surface-2 font-medium text-text-muted',
      sizes[size],
      className
    )}
    aria-hidden="true"
  >
    {toInitials(name)}
  </span>
{/if}
