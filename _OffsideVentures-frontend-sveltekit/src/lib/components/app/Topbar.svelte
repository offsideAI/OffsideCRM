<script lang="ts">
  import { ChevronDown, Menu as MenuIcon, Search, Sparkles } from 'lucide-svelte';
  import type { CurrentUser } from '$lib/api/schemas';
  import { Menu, MenuItem } from '$lib/components/ui';
  import { initials } from '$lib/utils/format';

  interface Props {
    user: CurrentUser;
    onMenu?: () => void;
    onSearch?: () => void;
    onAi?: () => void;
  }

  let { user, onMenu, onSearch, onAi }: Props = $props();

  const displayName = $derived(`${user.first_name} ${user.last_name}`.trim() || user.email);

  async function signOut() {
    await fetch('/auth/logout', { method: 'POST' });
    window.location.href = '/login';
  }
</script>

<header class="flex h-14 shrink-0 items-center gap-3 border-b border-border bg-surface-0 px-4">
  <button
    onclick={onMenu}
    class="rounded-md p-1.5 text-text-muted transition-colors hover:bg-surface-2 hover:text-text lg:hidden"
    aria-label="Open navigation"
  >
    <MenuIcon class="h-5 w-5" />
  </button>

  <button
    onclick={onSearch}
    class="flex h-9 w-full max-w-md items-center gap-2 rounded-lg border border-border bg-surface-1 px-3 text-sm text-text-subtle transition-colors hover:border-border-strong"
  >
    <Search class="h-4 w-4" />
    <span>Search…</span>
    <kbd
      class="ml-auto hidden rounded border border-border bg-surface-2 px-1.5 py-0.5 font-mono text-[10px] text-text-subtle sm:inline"
    >
      ⌘K
    </kbd>
  </button>

  <div class="ml-auto flex items-center gap-2">
    <button
      onclick={onAi}
      class="inline-flex h-9 items-center gap-1.5 rounded-lg border border-accent/30 bg-accent/10 px-3 text-sm font-medium text-accent transition-colors hover:bg-accent/15"
    >
      <Sparkles class="h-4 w-4" />
      <span class="hidden sm:inline">Ask AI</span>
    </button>

    <Menu>
      {#snippet trigger()}
        <span
          class="inline-flex h-9 items-center gap-1.5 rounded-lg px-2 text-sm text-text-muted transition-colors hover:bg-surface-2"
        >
          <span
            class="grid h-6 w-6 place-items-center rounded-full border border-border bg-surface-2 text-[0.7rem] font-medium text-text-muted"
          >
            {initials(displayName)}
          </span>
          <ChevronDown class="h-3.5 w-3.5" />
        </span>
      {/snippet}
      <div class="px-2 py-1.5 text-xs text-text-subtle">{user.email}</div>
      <MenuItem>Profile</MenuItem>
      <MenuItem>Settings</MenuItem>
      <MenuItem tone="danger" onSelect={signOut}>Sign out</MenuItem>
    </Menu>
  </div>
</header>
