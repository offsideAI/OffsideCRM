<script lang="ts">
  import { StickyNote } from 'lucide-svelte';
  import { EmptyState } from '$lib/components/ui';
</script>

<svelte:head><title>Notes · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">Notes &amp; activity</h1>
  <p class="mt-1 text-sm text-text-muted">Captured notes and the activity feed.</p>
  <div class="mt-6">
    <EmptyState
      title="Notes arrive in E8"
      description="Note capture plus a per-record and global activity feed land with the CRM screens milestone."
    >
      {#snippet icon()}<StickyNote class="h-5 w-5" />{/snippet}
    </EmptyState>
  </div>
</div>
