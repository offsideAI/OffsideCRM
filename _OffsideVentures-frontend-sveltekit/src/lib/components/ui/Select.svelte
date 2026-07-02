<script lang="ts">
  import { ChevronDown } from 'lucide-svelte';
  import type { HTMLSelectAttributes } from 'svelte/elements';
  import { cn } from '$lib/utils/cn';

  type Option = { value: string; label: string };

  interface Props extends HTMLSelectAttributes {
    value?: string;
    options?: Option[];
    placeholder?: string;
  }

  let {
    value = $bindable(''),
    options = [],
    placeholder,
    class: className,
    ...rest
  }: Props = $props();
</script>

<div class="relative">
  <select
    bind:value
    class={cn(
      'h-9 w-full appearance-none rounded-lg border border-border bg-surface-2 pl-3 pr-8 text-sm text-text outline-none transition-colors focus-visible:border-border-strong focus-visible:ring-2 focus-visible:ring-accent',
      className
    )}
    {...rest}
  >
    {#if placeholder}
      <option value="" disabled selected={!value}>{placeholder}</option>
    {/if}
    {#each options as option (option.value)}
      <option value={option.value}>{option.label}</option>
    {/each}
  </select>
  <ChevronDown
    class="pointer-events-none absolute right-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-text-subtle"
  />
</div>
