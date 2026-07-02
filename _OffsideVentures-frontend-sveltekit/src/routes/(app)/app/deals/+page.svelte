<script lang="ts">
  import { Handshake } from 'lucide-svelte';
  import { EmptyState } from '$lib/components/ui';
</script>

<svelte:head><title>Deals · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">Deals</h1>
  <p class="mt-1 text-sm text-text-muted">Opportunities moving through your pipeline.</p>
  <div class="mt-6">
    <EmptyState
      title="Pipeline arrives in E8"
      description="A kanban board by stage (drag to move) plus a table view and deal detail land with the CRM screens milestone."
    >
      {#snippet icon()}<Handshake class="h-5 w-5" />{/snippet}
    </EmptyState>
  </div>
</div>
