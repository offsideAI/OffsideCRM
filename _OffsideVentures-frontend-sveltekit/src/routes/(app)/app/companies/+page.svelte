<script lang="ts">
  import { Building2 } from 'lucide-svelte';
  import { EmptyState } from '$lib/components/ui';
</script>

<svelte:head><title>Companies · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">Companies</h1>
  <p class="mt-1 text-sm text-text-muted">Accounts you're tracking.</p>
  <div class="mt-6">
    <EmptyState
      title="Companies arrive in E8"
      description="The list (configurable columns, search, sort), detail view, timeline, and inline editing land with the CRM screens milestone."
    >
      {#snippet icon()}<Building2 class="h-5 w-5" />{/snippet}
    </EmptyState>
  </div>
</div>
