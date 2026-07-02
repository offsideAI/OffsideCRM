import * as fx from '$lib/mock/data';
import type { ApiResult } from './config';

// In-memory mock API used when MOCK is on. Mirrors the Django response shapes:
// companies/contacts/deals/tasks are paginated ({items,count}); notes/activities
// /pipelines return plain arrays.

let seq = 100_000;
const nowIso = () => new Date().toISOString();

const ok = (data: unknown): ApiResult => ({ status: 200, data });
const created = (data: unknown): ApiResult => ({ status: 201, data });
const notFound = (): ApiResult => ({ status: 404, data: { message: 'Not found (mock)' } });
const methodNotAllowed = (): ApiResult => ({ status: 405, data: { message: 'Method not allowed (mock)' } });

type Row = Record<string, unknown> & { id: number };

interface Collection {
  rows: Row[];
  paginated: boolean;
  filters?: string[];
  search?: (row: Row, needle: string) => boolean;
  template: Row;
}

function compare(a: unknown, b: unknown): number {
  if (a == null) return 1;
  if (b == null) return -1;
  if (typeof a === 'number' && typeof b === 'number') return a - b;
  return String(a).localeCompare(String(b));
}

function listOf(collection: Collection, params: URLSearchParams) {
  let rows = collection.rows.slice();
  const query = params.get('search');
  if (query && collection.search) {
    const needle = query.toLowerCase();
    rows = rows.filter((row) => collection.search!(row, needle));
  }
  for (const key of collection.filters ?? []) {
    const value = params.get(key);
    if (value != null && value !== '') rows = rows.filter((row) => String(row[key]) === value);
  }
  const ordering = params.get('ordering');
  if (ordering) {
    const desc = ordering.startsWith('-');
    const key = desc ? ordering.slice(1) : ordering;
    rows.sort((a, b) => compare(a[key], b[key]) * (desc ? -1 : 1));
  }
  const count = rows.length;
  const limit = Number(params.get('limit') ?? 50);
  const offset = Number(params.get('offset') ?? 0);
  return { items: rows.slice(offset, offset + limit), count };
}

const asRows = (value: unknown) => value as unknown as Row[];

const collections: Record<string, Collection> = {
  companies: {
    rows: asRows(fx.companies),
    paginated: true,
    filters: ['status'],
    search: (row, needle) => String(row.name).toLowerCase().includes(needle),
    template: asRows(fx.companies)[0]
  },
  contacts: {
    rows: asRows(fx.contacts),
    paginated: true,
    filters: ['status', 'company_id'],
    search: (row, needle) => String(row.full_name).toLowerCase().includes(needle),
    template: asRows(fx.contacts)[0]
  },
  deals: {
    rows: asRows(fx.deals),
    paginated: true,
    filters: ['status', 'stage_id', 'company_id', 'pipeline_id'],
    search: (row, needle) => String(row.name).toLowerCase().includes(needle),
    template: asRows(fx.deals)[0]
  },
  tasks: {
    rows: asRows(fx.tasks),
    paginated: true,
    filters: ['status', 'company_id', 'contact_id', 'deal_id'],
    template: asRows(fx.tasks)[0]
  },
  notes: {
    rows: asRows(fx.notes),
    paginated: false,
    filters: ['company_id', 'contact_id', 'deal_id'],
    template: asRows(fx.notes)[0]
  },
  activities: {
    rows: asRows(fx.activities),
    paginated: false,
    filters: ['company_id', 'contact_id', 'deal_id'],
    template: asRows(fx.activities)[0]
  }
};

function mockSearch(query: string) {
  const needle = query.toLowerCase();
  return {
    companies: fx.companies
      .filter((c) => c.name.toLowerCase().includes(needle))
      .slice(0, 5)
      .map((c) => ({ id: c.id, name: c.name })),
    contacts: fx.contacts
      .filter((c) => c.full_name.toLowerCase().includes(needle))
      .slice(0, 5)
      .map((c) => ({ id: c.id, name: c.full_name, email: c.email })),
    deals: fx.deals
      .filter((d) => d.name.toLowerCase().includes(needle))
      .slice(0, 5)
      .map((d) => ({ id: d.id, name: d.name }))
  };
}

function mockAi(action: string): ApiResult {
  const note =
    '[mock-ai] AI provider not configured; this is placeholder text so the UI is fully usable.';
  switch (action) {
    case 'assistant':
      return ok({ reply: note, agent_action_id: 0, provider: 'mock', model: 'mock' });
    case 'summarize':
      return ok({ text: note, agent_action_id: 0 });
    case 'draft-email':
      return ok({ subject: 'Quick follow-up', body: note, agent_action_id: 0 });
    case 'score-lead':
      return ok({ score: 65, rationale: note, agent_action_id: 0 });
    case 'classify':
      return ok({ category: 'Warm Lead', rationale: note, agent_action_id: 0 });
    default:
      return ok({ message: note });
  }
}

export function mockRequest(
  method: string,
  pathname: string,
  params: URLSearchParams,
  body?: string
): ApiResult {
  const segments = pathname.replace(/^\/+|\/+$/g, '').split('/').filter(Boolean);
  const [resource, second] = segments;
  let payload: Record<string, unknown> | undefined;
  if (body) {
    try {
      payload = JSON.parse(body) as Record<string, unknown>;
    } catch {
      payload = undefined;
    }
  }

  if (resource === 'me') return ok(fx.mockUser);
  if (resource === 'search') return ok(mockSearch(params.get('q') ?? ''));
  if (resource === 'pipelines') return ok(fx.pipelines);
  if (resource === 'ai') return mockAi(second ?? '');

  const collection = collections[resource];
  if (!collection) return notFound();

  if (!second) {
    if (method === 'GET') {
      const list = listOf(collection, params);
      return ok(collection.paginated ? list : list.items);
    }
    if (method === 'POST') {
      const row = {
        ...collection.template,
        ...(payload ?? {}),
        id: ++seq,
        created_at: nowIso(),
        updated_at: nowIso()
      } as Row;
      collection.rows.push(row);
      return created(row);
    }
    return methodNotAllowed();
  }

  const id = Number(second);
  const row = collection.rows.find((r) => r.id === id);
  if (method === 'GET') return row ? ok(row) : notFound();
  if (method === 'PATCH' || method === 'PUT') {
    if (!row) return notFound();
    Object.assign(row, payload ?? {}, { updated_at: nowIso() });
    return ok(row);
  }
  if (method === 'DELETE') {
    const index = collection.rows.findIndex((r) => r.id === id);
    if (index >= 0) collection.rows.splice(index, 1);
    return { status: 204, data: null };
  }
  return methodNotAllowed();
}
