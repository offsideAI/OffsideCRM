import { z } from 'zod';

// Zod schemas mirror the Django Ninja output shapes (core/schemas.py). Inferred
// types are the single source of truth the UI relies on; parsing at the API
// boundary keeps the frontend honest if the backend drifts.

export const currentUserSchema = z.object({
  id: z.number(),
  email: z.string(),
  first_name: z.string().default(''),
  last_name: z.string().default('')
});
export type CurrentUser = z.infer<typeof currentUserSchema>;

export const companySchema = z.object({
  id: z.number(),
  name: z.string(),
  domain: z.string(),
  industry: z.string(),
  size: z.string(),
  status: z.string(),
  description: z.string(),
  phone: z.string(),
  email: z.string(),
  linkedin_url: z.string(),
  logo_url: z.string(),
  annual_revenue: z.number().nullable(),
  street: z.string(),
  city: z.string(),
  state: z.string(),
  postal_code: z.string(),
  country: z.string(),
  owner_id: z.number().nullable(),
  contacts_count: z.number(),
  deals_count: z.number(),
  created_at: z.string(),
  updated_at: z.string()
});
export type Company = z.infer<typeof companySchema>;

export const contactSchema = z.object({
  id: z.number(),
  first_name: z.string(),
  last_name: z.string(),
  full_name: z.string(),
  email: z.string(),
  phone: z.string(),
  job_title: z.string(),
  status: z.string(),
  linkedin_url: z.string(),
  company_id: z.number().nullable(),
  company_name: z.string().nullable(),
  owner_id: z.number().nullable(),
  created_at: z.string(),
  updated_at: z.string()
});
export type Contact = z.infer<typeof contactSchema>;

export const stageSchema = z.object({
  id: z.number(),
  pipeline_id: z.number(),
  name: z.string(),
  order: z.number(),
  probability: z.number(),
  is_won: z.boolean(),
  is_lost: z.boolean()
});
export type Stage = z.infer<typeof stageSchema>;

export const pipelineSchema = z.object({
  id: z.number(),
  name: z.string(),
  is_default: z.boolean(),
  stages: z.array(stageSchema)
});
export type Pipeline = z.infer<typeof pipelineSchema>;

export const dealSchema = z.object({
  id: z.number(),
  name: z.string(),
  company_id: z.number().nullable(),
  company_name: z.string().nullable(),
  primary_contact_id: z.number().nullable(),
  primary_contact_name: z.string().nullable(),
  pipeline_id: z.number(),
  stage_id: z.number(),
  stage_name: z.string().nullable(),
  amount: z.number(),
  currency: z.string(),
  status: z.string(),
  close_date: z.string().nullable(),
  description: z.string(),
  owner_id: z.number().nullable(),
  created_at: z.string(),
  updated_at: z.string()
});
export type Deal = z.infer<typeof dealSchema>;

export const taskSchema = z.object({
  id: z.number(),
  title: z.string(),
  description: z.string(),
  status: z.string(),
  priority: z.string(),
  due_date: z.string().nullable(),
  completed_at: z.string().nullable(),
  assignee_id: z.number().nullable(),
  company_id: z.number().nullable(),
  contact_id: z.number().nullable(),
  deal_id: z.number().nullable(),
  created_at: z.string(),
  updated_at: z.string()
});
export type Task = z.infer<typeof taskSchema>;

export const noteSchema = z.object({
  id: z.number(),
  body: z.string(),
  author_id: z.number().nullable(),
  company_id: z.number().nullable(),
  contact_id: z.number().nullable(),
  deal_id: z.number().nullable(),
  created_at: z.string(),
  updated_at: z.string()
});
export type Note = z.infer<typeof noteSchema>;

export const activitySchema = z.object({
  id: z.number(),
  type: z.string(),
  summary: z.string(),
  body: z.string(),
  actor_id: z.number().nullable(),
  occurred_at: z.string(),
  company_id: z.number().nullable(),
  contact_id: z.number().nullable(),
  deal_id: z.number().nullable(),
  created_at: z.string()
});
export type Activity = z.infer<typeof activitySchema>;

/** Wrap an item schema into Django Ninja's `{ items, count }` paginated shape. */
export const paginatedSchema = <T extends z.ZodTypeAny>(item: T) =>
  z.object({ items: z.array(item), count: z.number() });
