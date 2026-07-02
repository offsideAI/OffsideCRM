<script lang="ts">
  import { Search } from 'lucide-svelte';
  import type { Snippet } from 'svelte';
  import Dialog from './Dialog.svelte';

  // Command-palette shell. E10 wires real search + keyboard navigation;
  // this provides the surface, the query input, and a results slot.
  interface Props {
    open?: boolean;
    query?: string;
    placeholder?: string;
    children?: Snippet;
  }

  let {
    open = $bindable(false),
    query = $bindable(''),
    placeholder = 'Search or run a command…',
    children
  }: Props = $props();
</script>

<Dialog bind:open class="max-w-xl p-0">
  <div class="flex items-center gap-2 border-b border-border px-3">
    <Search class="h-4 w-4 shrink-0 text-text-subtle" />
    <input
      bind:value={query}
      {placeholder}
      class="h-11 w-full bg-transparent text-sm text-text outline-none placeholder:text-text-subtle"
    />
  </div>
  <div class="max-h-80 overflow-y-auto p-2">
    {#if children}
      {@render children()}
    {:else}
      <p class="px-2 py-6 text-center text-sm text-text-subtle">Start typing to search…</p>
    {/if}
  </div>
</Dialog>
