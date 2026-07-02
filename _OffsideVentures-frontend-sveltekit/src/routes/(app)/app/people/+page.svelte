<script lang="ts">
  import { Users } from 'lucide-svelte';
  import { EmptyState } from '$lib/components/ui';
</script>

<svelte:head><title>People · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">People</h1>
  <p class="mt-1 text-sm text-text-muted">Contacts across your accounts.</p>
  <div class="mt-6">
    <EmptyState
      title="Contacts arrive in E8"
      description="List and detail views, with company links and activity timelines, land with the CRM screens milestone."
    >
      {#snippet icon()}<Users class="h-5 w-5" />{/snippet}
    </EmptyState>
  </div>
</div>
