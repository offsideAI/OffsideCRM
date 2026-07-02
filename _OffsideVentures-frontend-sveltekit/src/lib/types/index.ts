import type { ComponentType } from 'svelte';

// Re-export the canonical CurrentUser (defined alongside the Zod schemas).
export type { CurrentUser } from '$lib/api/schemas';

export type ID = number;

/** A renderable icon component (lucide-svelte ships legacy class components). */
export type IconComponent = ComponentType;

/** Shape of a Django Ninja limit/offset paginated list response. */
export interface Paginated<T> {
  items: T[];
  count: number;
}
