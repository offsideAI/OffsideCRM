<script lang="ts">
  import { page } from '$app/state';
  import { footerNavItems, navItems } from '$lib/config/nav';
  import { cn } from '$lib/utils/cn';

  interface Props {
    onNavigate?: () => void;
    collapsed?: boolean;
  }

  let { onNavigate, collapsed = false }: Props = $props();

  function isActive(href: string): boolean {
    return page.url.pathname === href || page.url.pathname.startsWith(href + '/');
  }

  const linkClass = (href: string) =>
    cn(
      'flex items-center gap-2.5 rounded-lg py-2 text-sm font-medium transition-colors',
      collapsed ? 'justify-center px-0' : 'px-2.5',
      isActive(href)
        ? 'bg-surface-2 text-text'
        : 'text-text-muted hover:bg-surface-2 hover:text-text'
    );
</script>

<nav class="flex flex-1 flex-col gap-0.5">
  {#each navItems as item (item.href)}
    {@const Icon = item.icon}
    <a
      href={item.href}
      onclick={onNavigate}
      title={collapsed ? item.label : undefined}
      class={linkClass(item.href)}
      aria-current={isActive(item.href) ? 'page' : undefined}
    >
      <Icon class="h-4 w-4 shrink-0" />
      {#if !collapsed}{item.label}{/if}
    </a>
  {/each}

  <div class="flex-1"></div>

  {#each footerNavItems as item (item.href)}
    {@const Icon = item.icon}
    <a
      href={item.href}
      onclick={onNavigate}
      title={collapsed ? item.label : undefined}
      class={linkClass(item.href)}
      aria-current={isActive(item.href) ? 'page' : undefined}
    >
      <Icon class="h-4 w-4 shrink-0" />
      {#if !collapsed}{item.label}{/if}
    </a>
  {/each}
</nav>
