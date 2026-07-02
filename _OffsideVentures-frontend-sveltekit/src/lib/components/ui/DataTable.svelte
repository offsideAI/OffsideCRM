<script lang="ts" generics="TRow">
  import { ChevronDown, ChevronsUpDown, ChevronUp } from 'lucide-svelte';
  import type { Snippet } from 'svelte';
  import { cn } from '$lib/utils/cn';

  type Column = {
    key: string;
    label: string;
    sortable?: boolean;
    align?: 'left' | 'right' | 'center';
    width?: string;
  };

  interface Props {
    columns: Column[];
    rows: TRow[];
    getKey?: (row: TRow, index: number) => string | number;
    accessor?: (row: TRow, key: string) => unknown;
    cell?: Snippet<[{ row: TRow; key: string }]>;
    onRowClick?: (row: TRow) => void;
    class?: string;
  }

  let {
    columns,
    rows,
    getKey = (_row, index) => index,
    accessor = (row, key) => (row as Record<string, unknown>)[key],
    cell,
    onRowClick,
    class: className
  }: Props = $props();

  let sortKey = $state<string | null>(null);
  let sortDir = $state<'asc' | 'desc'>('asc');

  function toggleSort(key: string) {
    if (sortKey === key) {
      sortDir = sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey = key;
      sortDir = 'asc';
    }
  }

  function compare(a: unknown, b: unknown): number {
    if (a == null) return 1;
    if (b == null) return -1;
    if (typeof a === 'number' && typeof b === 'number') return a - b;
    return String(a).localeCompare(String(b));
  }

  const sorted = $derived.by(() => {
    if (!sortKey) return rows;
    const key = sortKey;
    const direction = sortDir === 'asc' ? 1 : -1;
    return [...rows].sort((a, b) => compare(accessor(a, key), accessor(b, key)) * direction);
  });

  const alignClass = { left: 'text-left', right: 'text-right', center: 'text-center' };
</script>

<div class={cn('overflow-hidden rounded-xl border border-border', className)}>
  <table class="w-full border-collapse text-sm">
    <thead>
      <tr class="border-b border-border bg-surface-1">
        {#each columns as col (col.key)}
          <th
            class={cn('px-3 py-2.5 font-medium text-text-muted', alignClass[col.align ?? 'left'])}
            style={col.width ? `width:${col.width}` : undefined}
          >
            {#if col.sortable}
              <button
                onclick={() => toggleSort(col.key)}
                class="inline-flex items-center gap-1 transition-colors hover:text-text"
              >
                {col.label}
                {#if sortKey === col.key}
                  {#if sortDir === 'asc'}
                    <ChevronUp class="h-3.5 w-3.5" />
                  {:else}
                    <ChevronDown class="h-3.5 w-3.5" />
                  {/if}
                {:else}
                  <ChevronsUpDown class="h-3.5 w-3.5 opacity-40" />
                {/if}
              </button>
            {:else}
              {col.label}
            {/if}
          </th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each sorted as row, index (getKey(row, index))}
        <tr
          class={cn(
            'border-b border-border transition-colors last:border-0',
            onRowClick && 'cursor-pointer hover:bg-surface-1'
          )}
          onclick={() => onRowClick?.(row)}
        >
          {#each columns as col (col.key)}
            <td class={cn('px-3 py-2.5 text-text', alignClass[col.align ?? 'left'])}>
              {#if cell}
                {@render cell({ row, key: col.key })}
              {:else}
                {String(accessor(row, col.key) ?? '—')}
              {/if}
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
</div>
