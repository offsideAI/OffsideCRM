import type {
  Activity,
  Company,
  Contact,
  CurrentUser,
  Deal,
  Note,
  Pipeline,
  Task
} from '$lib/api/schemas';

// Realistic in-memory fixtures for mock mode (mirrors the Django seed_demo).
const T = '2026-01-15T12:00:00Z';

export const mockUser: CurrentUser = {
  id: 1,
  email: 'demo@offsideventures.com',
  first_name: 'Demo',
  last_name: 'User'
};

function company(id: number, name: string, over: Partial<Company> = {}): Company {
  return {
    id,
    name,
    domain: '',
    industry: '',
    size: '',
    status: 'prospect',
    description: '',
    phone: '',
    email: '',
    linkedin_url: '',
    logo_url: '',
    annual_revenue: null,
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
    owner_id: 1,
    contacts_count: 0,
    deals_count: 0,
    created_at: T,
    updated_at: T,
    ...over
  };
}

export const companies: Company[] = [
  company(1, 'Northwind Labs', { domain: 'northwindlabs.com', industry: 'Biotech', size: '51-200', status: 'active', city: 'Boston', country: 'USA', contacts_count: 2, deals_count: 1 }),
  company(2, 'Helio Freight', { domain: 'heliofreight.com', industry: 'Logistics', size: '201-1000', status: 'customer', city: 'Rotterdam', country: 'Netherlands', contacts_count: 2, deals_count: 1 }),
  company(3, 'Cobalt Studio', { domain: 'cobalt.studio', industry: 'Design', size: '11-50', status: 'prospect', city: 'Lisbon', country: 'Portugal', contacts_count: 1, deals_count: 1 }),
  company(4, 'Meridian Capital', { domain: 'meridiancap.com', industry: 'Finance', size: '1000+', status: 'active', city: 'New York', country: 'USA', contacts_count: 2, deals_count: 1 }),
  company(5, 'Tindr Robotics', { domain: 'tindr.io', industry: 'Manufacturing', size: '51-200', status: 'prospect', city: 'Munich', country: 'Germany', contacts_count: 1, deals_count: 1 }),
  company(6, 'Vela Health', { domain: 'velahealth.com', industry: 'Healthcare', size: '11-50', status: 'customer', city: 'Austin', country: 'USA', contacts_count: 1, deals_count: 1 })
];

function contact(id: number, first: string, last: string, companyId: number, over: Partial<Contact> = {}): Contact {
  const companyName = companies.find((c) => c.id === companyId)?.name ?? null;
  return {
    id,
    first_name: first,
    last_name: last,
    full_name: `${first} ${last}`.trim(),
    email: `${first.toLowerCase()}@example.com`,
    phone: '',
    job_title: '',
    status: 'lead',
    linkedin_url: '',
    company_id: companyId,
    company_name: companyName,
    owner_id: 1,
    created_at: T,
    updated_at: T,
    ...over
  };
}

export const contacts: Contact[] = [
  contact(1, 'Ada', 'Reyes', 1, { job_title: 'VP Engineering', status: 'active' }),
  contact(2, 'Marcus', 'Lin', 1, { job_title: 'Procurement Lead' }),
  contact(3, 'Sofia', 'Okonkwo', 2, { job_title: 'COO', status: 'customer' }),
  contact(4, 'Idris', 'Khan', 2, { job_title: 'Ops Manager', status: 'active' }),
  contact(5, 'Lena', 'Vasquez', 3, { job_title: 'Founder' }),
  contact(6, 'Tom', 'Becker', 4, { job_title: 'Managing Director', status: 'active' }),
  contact(7, 'Hannah', 'Stein', 5, { job_title: 'Head of Product' }),
  contact(8, 'Diego', 'Moreno', 6, { job_title: 'CEO', status: 'customer' })
];

export const pipelines: Pipeline[] = [
  {
    id: 1,
    name: 'Sales Pipeline',
    is_default: true,
    stages: [
      { id: 1, pipeline_id: 1, name: 'New', order: 0, probability: 10, is_won: false, is_lost: false },
      { id: 2, pipeline_id: 1, name: 'Qualified', order: 1, probability: 30, is_won: false, is_lost: false },
      { id: 3, pipeline_id: 1, name: 'Proposal', order: 2, probability: 55, is_won: false, is_lost: false },
      { id: 4, pipeline_id: 1, name: 'Negotiation', order: 3, probability: 75, is_won: false, is_lost: false },
      { id: 5, pipeline_id: 1, name: 'Closed Won', order: 4, probability: 100, is_won: true, is_lost: false },
      { id: 6, pipeline_id: 1, name: 'Closed Lost', order: 5, probability: 0, is_won: false, is_lost: true }
    ]
  }
];

function deal(id: number, name: string, companyId: number, contactId: number, stageId: number, amount: number, over: Partial<Deal> = {}): Deal {
  const stage = pipelines[0].stages.find((s) => s.id === stageId);
  return {
    id,
    name,
    company_id: companyId,
    company_name: companies.find((c) => c.id === companyId)?.name ?? null,
    primary_contact_id: contactId,
    primary_contact_name: contacts.find((c) => c.id === contactId)?.full_name ?? null,
    pipeline_id: 1,
    stage_id: stageId,
    stage_name: stage?.name ?? null,
    amount,
    currency: 'USD',
    status: stage?.is_won ? 'won' : 'open',
    close_date: '2026-03-01',
    description: '',
    owner_id: 1,
    created_at: T,
    updated_at: T,
    ...over
  };
}

export const deals: Deal[] = [
  deal(1, 'Northwind platform rollout', 1, 1, 3, 48000),
  deal(2, 'Helio annual renewal', 2, 3, 5, 120000),
  deal(3, 'Cobalt brand retainer', 3, 5, 2, 18000),
  deal(4, 'Meridian data platform', 4, 6, 4, 240000),
  deal(5, 'Tindr pilot program', 5, 7, 1, 32000),
  deal(6, 'Vela expansion', 6, 8, 3, 56000)
];

export const tasks: Task[] = [
  { id: 1, title: 'Send Northwind proposal', description: '', status: 'todo', priority: 'high', due_date: '2026-01-20T17:00:00Z', completed_at: null, assignee_id: 1, company_id: 1, contact_id: 1, deal_id: 1, created_at: T, updated_at: T },
  { id: 2, title: 'Prep Meridian security review', description: '', status: 'todo', priority: 'medium', due_date: '2026-01-24T17:00:00Z', completed_at: null, assignee_id: 1, company_id: 4, contact_id: null, deal_id: 4, created_at: T, updated_at: T },
  { id: 3, title: 'Follow up with Cobalt', description: '', status: 'in_progress', priority: 'medium', due_date: null, completed_at: null, assignee_id: 1, company_id: 3, contact_id: 5, deal_id: 3, created_at: T, updated_at: T },
  { id: 4, title: 'Schedule Vela kickoff', description: '', status: 'done', priority: 'low', due_date: null, completed_at: T, assignee_id: 1, company_id: 6, contact_id: 8, deal_id: 6, created_at: T, updated_at: T }
];

export const notes: Note[] = [
  { id: 1, body: 'Champion is Ada; budget confirmed for Q3.', author_id: 1, company_id: 1, contact_id: 1, deal_id: 1, created_at: T, updated_at: T },
  { id: 2, body: 'Helio renewal looks healthy — usage up 20%.', author_id: 1, company_id: 2, contact_id: null, deal_id: 2, created_at: T, updated_at: T }
];

export const activities: Activity[] = [
  { id: 1, type: 'system', summary: "Deal 'Northwind platform rollout' created", body: '', actor_id: 1, occurred_at: T, company_id: 1, contact_id: null, deal_id: 1, created_at: T },
  { id: 2, type: 'call', summary: 'Discovery call with Sofia', body: '', actor_id: 1, occurred_at: T, company_id: 2, contact_id: 3, deal_id: 2, created_at: T },
  { id: 3, type: 'email', summary: 'Sent pricing to Meridian', body: '', actor_id: 1, occurred_at: T, company_id: 4, contact_id: 6, deal_id: 4, created_at: T }
];
