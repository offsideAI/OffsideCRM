<script lang="ts">
  import { Sparkles } from 'lucide-svelte';
  import { EmptyState } from '$lib/components/ui';
</script>

<svelte:head><title>AI Copilot · OffsideVentures</title></svelte:head>

<div class="px-6 py-6">
  <h1 class="text-lg font-semibold text-text">AI Copilot</h1>
  <p class="mt-1 text-sm text-text-muted">Your agentic assistant over CRM data.</p>
  <div class="mt-6">
    <EmptyState
      title="The Copilot arrives in E9"
      description="A full chat surface with record context, suggested actions (summarize, draft email, score lead, create task), human-confirm before writes, and an agent audit trail."
    >
      {#snippet icon()}<Sparkles class="h-5 w-5" />{/snippet}
    </EmptyState>
  </div>
</div>
