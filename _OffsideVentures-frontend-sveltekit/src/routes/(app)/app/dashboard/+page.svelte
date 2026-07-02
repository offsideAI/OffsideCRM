<script lang="ts">
  import { Building2, Handshake, ListChecks, TrendingUp } from 'lucide-svelte';
  import { Card } from '$lib/components/ui';
  import { formatCurrency } from '$lib/utils/format';
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  const stats = $derived([
    { label: 'Pipeline value', value: formatCurrency(data.stats.pipelineValue), icon: TrendingUp },
    { label: 'Open deals', value: String(data.stats.openDeals), icon: Handshake },
    { label: 'Tasks due', value: String(data.stats.tasksDue), icon: ListChecks },
    { label: 'Companies', value: String(data.stats.companies), icon: Building2 }
  ]);
</script>

<svelte:head><title>Dashboard · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">Good to see you</h1>
  <p class="mt-1 text-sm text-text-muted">Here's what's happening across your pipeline.</p>

  <div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
    {#each stats as stat (stat.label)}
      {@const Icon = stat.icon}
      <Card class="p-4">
        <div class="flex items-center justify-between">
          <span class="text-sm text-text-muted">{stat.label}</span>
          <Icon class="h-4 w-4 text-text-subtle" />
        </div>
        <p class="mt-2 text-2xl font-semibold tracking-tight text-text">{stat.value}</p>
      </Card>
    {/each}
  </div>

  <div class="mt-6 grid gap-4 lg:grid-cols-3">
    <Card class="p-5 lg:col-span-2">
      <h2 class="text-sm font-medium text-text">Recent activity</h2>
      <p class="mt-4 text-sm text-text-subtle">
        The activity timeline appears with the record screens (E8).
      </p>
    </Card>
    <Card class="p-5">
      <h2 class="text-sm font-medium text-text">Ask AI</h2>
      <p class="mt-2 text-sm text-text-muted">
        Use “Ask AI” in the top bar to summarize records, draft follow-ups, and create tasks (E9).
      </p>
    </Card>
  </div>
</div>
