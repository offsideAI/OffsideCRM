<script lang="ts">
  import { Avatar, Badge, Button, Card, EmptyState, Input, Skeleton } from '$lib/components/ui';
  import { ArrowUpRight, Inbox, Sparkles } from 'lucide-svelte';

  const surfaces = ['--surface-0', '--surface-1', '--surface-2', '--surface-3'];
  const accents = ['--accent', '--success', '--warning', '--info'];
</script>

<svelte:head>
  <title>OffsideVentures — Design System</title>
</svelte:head>

<div class="mx-auto min-h-screen max-w-5xl px-6 py-16">
  <header class="flex items-center justify-between">
    <div class="flex items-center gap-2.5">
      <span class="grid h-7 w-7 place-items-center rounded-md bg-surface-2 ring-1 ring-border">
        <span class="h-2 w-2 rounded-[2px] bg-accent"></span>
      </span>
      <span class="text-[0.95rem] font-semibold tracking-tight">OffsideVentures</span>
    </div>
    <Badge tone="accent"><Sparkles class="h-3 w-3" /> Agentic CRM</Badge>
  </header>

  <section class="mt-16 max-w-2xl">
    <p class="font-mono text-xs uppercase tracking-[0.2em] text-text-subtle">Design system · v0.1</p>
    <h1 class="mt-4 text-4xl font-semibold leading-[1.1] tracking-tight text-text sm:text-5xl">
      A calm, fast CRM with AI as a first-class collaborator.
    </h1>
    <p class="mt-5 max-w-xl text-[0.975rem] leading-relaxed text-text-muted">
      Monochrome surfaces, hairline borders, and a single signal-red accent used as rare
      punctuation. This page renders the foundational tokens and primitives.
    </p>
    <div class="mt-7 flex flex-wrap items-center gap-3">
      <a
        href="/app/dashboard"
        class="inline-flex h-9 items-center gap-2 rounded-lg bg-accent px-4 text-sm font-medium text-accent-contrast transition-colors hover:bg-accent-hover"
      >
        Open app <ArrowUpRight class="h-4 w-4" />
      </a>
      <Button variant="outline">View components</Button>
    </div>
  </section>

  <section class="mt-16">
    <h2 class="text-sm font-medium text-text-muted">Palette</h2>
    <div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
      {#each surfaces as token (token)}
        <div class="rounded-lg border border-border p-3">
          <div class="h-12 rounded-md border border-border" style="background: var({token})"></div>
          <p class="mt-2 font-mono text-xs text-text-subtle">{token}</p>
        </div>
      {/each}
    </div>
    <div class="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
      {#each accents as token (token)}
        <div class="rounded-lg border border-border p-3">
          <div class="h-12 rounded-md" style="background: var({token})"></div>
          <p class="mt-2 font-mono text-xs text-text-subtle">{token}</p>
        </div>
      {/each}
    </div>
  </section>

  <section class="mt-16 grid gap-6 lg:grid-cols-2">
    <Card class="p-5">
      <h3 class="text-sm font-medium">Buttons</h3>
      <div class="mt-4 flex flex-wrap gap-2">
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="ghost">Ghost</Button>
        <Button variant="danger">Danger</Button>
      </div>
      <div class="mt-4 flex flex-wrap items-center gap-2">
        <Button size="sm">Small</Button>
        <Button size="md">Medium</Button>
        <Button size="lg">Large</Button>
        <Button variant="outline" disabled>Disabled</Button>
      </div>
    </Card>

    <Card class="p-5">
      <h3 class="text-sm font-medium">Badges &amp; input</h3>
      <div class="mt-4 flex flex-wrap gap-2">
        <Badge>Neutral</Badge>
        <Badge tone="accent">Accent</Badge>
        <Badge tone="success">Won</Badge>
        <Badge tone="warning">At risk</Badge>
        <Badge tone="danger">Lost</Badge>
        <Badge tone="info">Lead</Badge>
      </div>
      <div class="mt-5">
        <Input placeholder="Search companies…" />
      </div>
    </Card>

    <Card class="p-5">
      <h3 class="text-sm font-medium">Record row</h3>
      <div class="mt-4 flex items-center gap-3">
        <Avatar name="Ada Reyes" />
        <div class="min-w-0">
          <p class="truncate text-sm font-medium">Ada Reyes</p>
          <p class="truncate text-xs text-text-subtle">VP Engineering · Northwind Labs</p>
        </div>
        <Badge tone="success" class="ml-auto">Active</Badge>
      </div>
      <h3 class="mt-6 text-sm font-medium">Loading</h3>
      <div class="mt-3 space-y-2">
        <Skeleton class="h-4 w-2/3" />
        <Skeleton class="h-4 w-1/2" />
      </div>
    </Card>

    <EmptyState title="No deals yet" description="Create your first deal to start tracking pipeline.">
      {#snippet icon()}<Inbox class="h-5 w-5" />{/snippet}
      <Button variant="primary" size="sm">New deal</Button>
    </EmptyState>
  </section>

  <footer class="mt-16 border-t border-border pt-6 font-mono text-xs text-text-subtle">
    OffsideVentures · Monochrome + Signal Red · dark-first
  </footer>
</div>
