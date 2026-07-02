<script lang="ts">
  import { Tabs } from 'bits-ui';
  import { cn } from '$lib/utils/cn';

  type Tab = { value: string; label: string };

  interface Props {
    tabs: Tab[];
    value?: string;
    class?: string;
  }

  let { tabs, value = $bindable(tabs[0]?.value ?? ''), class: className }: Props = $props();
</script>

<Tabs.Root bind:value class={className}>
  <Tabs.List class="inline-flex items-center gap-1 rounded-lg border border-border bg-surface-1 p-1">
    {#each tabs as tab (tab.value)}
      <Tabs.Trigger
        value={tab.value}
        class="rounded-md px-3 py-1.5 text-sm font-medium text-text-muted outline-none transition-colors data-[state=active]:bg-surface-2 data-[state=active]:text-text"
      >
        {tab.label}
      </Tabs.Trigger>
    {/each}
  </Tabs.List>
</Tabs.Root>
