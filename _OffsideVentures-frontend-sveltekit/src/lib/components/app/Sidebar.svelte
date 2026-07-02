<script lang="ts">
  import { PanelLeft, PanelLeftClose } from 'lucide-svelte';
  import { ui } from '$lib/stores/ui.svelte';
  import { cn } from '$lib/utils/cn';
  import NavList from './NavList.svelte';
</script>

<aside
  class={cn(
    'flex h-full flex-col border-r border-border bg-surface-1 py-4 transition-[width] duration-150',
    ui.sidebarCollapsed ? 'w-16 px-2' : 'w-60 px-3'
  )}
>
  <a
    href="/app/dashboard"
    class={cn('mb-5 flex items-center gap-2.5', ui.sidebarCollapsed ? 'justify-center' : 'px-1.5')}
  >
    <span class="grid h-7 w-7 shrink-0 place-items-center rounded-md bg-surface-2 ring-1 ring-border">
      <span class="h-2 w-2 rounded-[2px] bg-accent"></span>
    </span>
    {#if !ui.sidebarCollapsed}
      <span class="text-[0.95rem] font-semibold tracking-tight text-text">OffsideVentures</span>
    {/if}
  </a>

  <NavList collapsed={ui.sidebarCollapsed} />

  <button
    onclick={() => ui.toggleSidebar()}
    title={ui.sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
    class={cn(
      'mt-2 flex items-center gap-2.5 rounded-lg py-2 text-sm font-medium text-text-subtle transition-colors hover:bg-surface-2 hover:text-text',
      ui.sidebarCollapsed ? 'justify-center px-0' : 'px-2.5'
    )}
  >
    {#if ui.sidebarCollapsed}
      <PanelLeft class="h-4 w-4 shrink-0" />
    {:else}
      <PanelLeftClose class="h-4 w-4 shrink-0" />
      Collapse
    {/if}
  </button>
</aside>
