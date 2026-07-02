<script lang="ts">
  import type { Snippet } from 'svelte';
  import type { HTMLButtonAttributes } from 'svelte/elements';
  import { cn } from '$lib/utils/cn';

  type Variant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  type Size = 'sm' | 'md' | 'lg' | 'icon';

  interface Props extends HTMLButtonAttributes {
    variant?: Variant;
    size?: Size;
    children?: Snippet;
  }

  let {
    variant = 'secondary',
    size = 'md',
    type = 'button',
    class: className,
    children,
    ...rest
  }: Props = $props();

  const variants: Record<Variant, string> = {
    primary: 'bg-accent text-accent-contrast hover:bg-accent-hover',
    secondary: 'border border-border bg-surface-2 text-text hover:bg-surface-3',
    outline: 'border border-border text-text hover:bg-surface-2',
    ghost: 'text-text-muted hover:bg-surface-2 hover:text-text',
    danger: 'bg-danger text-white hover:brightness-110'
  };

  const sizes: Record<Size, string> = {
    sm: 'h-8 gap-1.5 px-3 text-sm',
    md: 'h-9 gap-2 px-4 text-sm',
    lg: 'h-10 gap-2 px-5 text-[0.95rem]',
    icon: 'h-9 w-9'
  };
</script>

<button
  {type}
  class={cn(
    'inline-flex select-none items-center justify-center whitespace-nowrap rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent disabled:pointer-events-none disabled:opacity-50',
    variants[variant],
    sizes[size],
    className
  )}
  {...rest}
>
  {@render children?.()}
</button>
