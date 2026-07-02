<script lang="ts">
  import { ListChecks } from 'lucide-svelte';
  import { EmptyState } from '$lib/components/ui';
</script>

<svelte:head><title>Tasks · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">Tasks</h1>
  <p class="mt-1 text-sm text-text-muted">Your to-dos and follow-ups.</p>
  <div class="mt-6">
    <EmptyState
      title="Tasks arrive in E8"
      description="A list/board by status with due dates, priority, assignee, and record links lands with the CRM screens milestone."
    >
      {#snippet icon()}<ListChecks class="h-5 w-5" />{/snippet}
    </EmptyState>
  </div>
</div>
