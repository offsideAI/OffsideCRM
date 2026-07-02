<script lang="ts">
  import { Settings } from 'lucide-svelte';
  import { EmptyState } from '$lib/components/ui';
</script>

<svelte:head><title>Settings · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">Settings</h1>
  <p class="mt-1 text-sm text-text-muted">Profile and workspace configuration.</p>
  <div class="mt-6">
    <EmptyState
      title="Settings arrive in E8"
      description="Profile, workspace, and members/roles surfaces land with the CRM screens milestone."
    >
      {#snippet icon()}<Settings class="h-5 w-5" />{/snippet}
    </EmptyState>
  </div>
</div>
