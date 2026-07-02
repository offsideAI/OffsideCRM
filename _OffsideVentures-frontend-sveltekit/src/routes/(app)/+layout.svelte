<script lang="ts">
  import type { Snippet } from 'svelte';
  import NavList from '$lib/components/app/NavList.svelte';
  import Sidebar from '$lib/components/app/Sidebar.svelte';
  import Topbar from '$lib/components/app/Topbar.svelte';
  import { CommandPalette, Drawer } from '$lib/components/ui';
  import type { LayoutData } from './$types';

  let { children, data }: { children: Snippet; data: LayoutData } = $props();

  let commandOpen = $state(false);
  let aiOpen = $state(false);
  let mobileNavOpen = $state(false);

  function onKeydown(event: KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      commandOpen = !commandOpen;
    }
  }
</script>

<svelte:window onkeydown={onKeydown} />

<div class="flex h-screen overflow-hidden bg-surface-0">
  <div class="hidden lg:block">
    <Sidebar />
  </div>

  <div class="flex min-w-0 flex-1 flex-col">
    <Topbar
      user={data.user}
      onMenu={() => (mobileNavOpen = true)}
      onSearch={() => (commandOpen = true)}
      onAi={() => (aiOpen = true)}
    />
    <main class="flex-1 overflow-y-auto">
      {@render children()}
    </main>
  </div>
</div>

<!-- Mobile navigation -->
<Drawer bind:open={mobileNavOpen} side="left" title="OffsideVentures" class="max-w-xs">
  <NavList onNavigate={() => (mobileNavOpen = false)} />
</Drawer>

<!-- Global command palette (⌘K) -->
<CommandPalette bind:open={commandOpen} />

<!-- AI Copilot slide-over (shell — E9 fills it in) -->
<Drawer bind:open={aiOpen} title="AI Copilot">
  <p class="text-sm text-text-muted">
    The agentic AI assistant lands in E9. From here you'll ask about any record, generate
    follow-ups, summarize notes, score leads, and create tasks — with a human confirmation step
    before anything is written to the CRM.
  </p>
</Drawer>
