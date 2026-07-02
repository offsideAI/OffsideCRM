import { dealSchema, paginatedSchema } from '$lib/api/schemas';
import { apiRequest } from '$lib/server/api';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async (event) => {
  const [companiesRes, tasksRes, dealsRes] = await Promise.all([
    apiRequest(event, 'GET', 'companies/?limit=1'),
    apiRequest(event, 'GET', 'tasks/?status=todo&limit=1'),
    apiRequest(event, 'GET', 'deals/?limit=200')
  ]);

  const countOf = (result: { data: unknown }) =>
    result.data && typeof result.data === 'object' && 'count' in result.data
      ? Number((result.data as { count: number }).count)
      : 0;

  const dealsParsed = paginatedSchema(dealSchema).safeParse(dealsRes.data);
  const openDeals = dealsParsed.success ? dealsParsed.data.items.filter((d) => d.status === 'open') : [];
  const pipelineValue = openDeals.reduce((sum, deal) => sum + deal.amount, 0);

  return {
    stats: {
      companies: countOf(companiesRes),
      tasksDue: countOf(tasksRes),
      openDeals: openDeals.length,
      pipelineValue
    }
  };
};
