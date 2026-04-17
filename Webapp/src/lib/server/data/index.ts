import companiesData from './companies.json';

export type StockSymbol = {
	symbol?: string | null;
	exchange?: string | null;
	isin?: string | null;
};

export type Reason = {
	summary?: string | null;
	details?: string | null;
	source?: string | null;
	date_added?: string | null;
};

export type Company = {
	id: string;
	name: string;
	standard_name?: string | null;
	parent_company?: string | null;
	country_hq?: string | null;
	description?: string | null;
	industry?: string | null;
	booth_number?: string | null;
	confidence_score?: number | null;
	divestment_priority?: string | null;
	last_updated?: string | null;
	reasons?: Reason[];
	sources?: string[];
	data_sources?: string[];
	involvement_types?: string[];
	involvement_details?: string[];
	sectors?: string[];
	stock_symbols?: StockSymbol[];
	boycott_actions?: string[];
	alternatives?: string[];
	aliases?: string[];
};

type Dataset = {
	metadata: Record<string, unknown>;
	companies: Company[];
};

const dataset = companiesData as unknown as Dataset;

const companies: Company[] = (dataset.companies ?? []).slice().sort((a, b) =>
	(a.name ?? '').localeCompare(b.name ?? '', undefined, { sensitivity: 'base' })
);

const byId = new Map<string, Company>();
for (const c of companies) byId.set(c.id, c);

function lower(value: unknown): string {
	return typeof value === 'string' ? value.toLowerCase() : '';
}

const searchHaystacks: string[] = companies.map((c) => {
	const parts: string[] = [
		c.name,
		c.standard_name ?? '',
		c.description ?? '',
		c.industry ?? '',
		c.country_hq ?? '',
		c.parent_company ?? '',
		(c.involvement_types ?? []).join(' '),
		(c.sectors ?? []).join(' '),
		(c.aliases ?? []).join(' '),
		(c.reasons ?? [])
			.map((r) => `${r?.summary ?? ''} ${r?.details ?? ''}`)
			.join(' ')
	];
	return lower(parts.join(' \u0001 '));
});

function paginate<T>(items: T[], page: number, limit: number) {
	const total = items.length;
	const totalPages = Math.max(1, Math.ceil(total / limit));
	const safePage = Math.min(Math.max(1, page), totalPages);
	const offset = (safePage - 1) * limit;
	return {
		items: items.slice(offset, offset + limit),
		pagination: {
			page: safePage,
			limit,
			total,
			totalPages,
			hasNext: safePage < totalPages,
			hasPrev: safePage > 1
		}
	};
}

export type CompanySummary = Pick<
	Company,
	| 'id'
	| 'name'
	| 'description'
	| 'industry'
	| 'country_hq'
	| 'parent_company'
	| 'stock_symbols'
	| 'data_sources'
	| 'involvement_types'
	| 'sectors'
	| 'boycott_actions'
	| 'alternatives'
> & { sources: string[] };

function toSummary(c: Company): CompanySummary {
	return {
		id: c.id,
		name: c.name,
		description: c.description ?? null,
		industry: c.industry ?? null,
		country_hq: c.country_hq ?? null,
		parent_company: c.parent_company ?? null,
		stock_symbols: c.stock_symbols ?? [],
		data_sources: c.data_sources ?? [],
		involvement_types: c.involvement_types ?? [],
		sectors: c.sectors ?? [],
		boycott_actions: c.boycott_actions ?? [],
		alternatives: c.alternatives ?? [],
		sources: c.sources ?? []
	};
}

function searchIndices(query: string): number[] {
	const cleaned = query.trim().toLowerCase();
	if (!cleaned) return companies.map((_, i) => i);
	const tokens = cleaned.split(/\s+/).filter(Boolean);
	const out: number[] = [];
	for (let i = 0; i < searchHaystacks.length; i++) {
		const hay = searchHaystacks[i];
		let matches = true;
		for (const t of tokens) {
			if (!hay.includes(t)) {
				matches = false;
				break;
			}
		}
		if (matches) out.push(i);
	}
	return out;
}

export function searchCompanies({
	search = '',
	page = 1,
	limit = 20
}: {
	search?: string;
	page?: number;
	limit?: number;
}) {
	const indices = searchIndices(search);
	const matched = indices.map((i) => companies[i]);
	const { items, pagination } = paginate(matched, page, limit);
	return {
		companies: items.map(toSummary),
		pagination
	};
}

export function getCompanyById(id: string): Company | null {
	const c = byId.get(id);
	if (!c) return null;
	return {
		...c,
		stock_symbols: c.stock_symbols ?? [],
		sources: c.sources ?? [],
		data_sources: c.data_sources ?? [],
		reasons: c.reasons ?? [],
		involvement_types: c.involvement_types ?? [],
		sectors: c.sectors ?? [],
		boycott_actions: c.boycott_actions ?? [],
		alternatives: c.alternatives ?? [],
		aliases: c.aliases ?? []
	};
}

export function findByInvolvement(type: string, page = 1, limit = 20) {
	const target = type.toLowerCase();
	const matched = companies
		.filter((c) => (c.involvement_types ?? []).some((t) => t.toLowerCase() === target))
		.slice()
		.sort((a, b) => {
			const sa = a.confidence_score ?? -Infinity;
			const sb = b.confidence_score ?? -Infinity;
			if (sa !== sb) return sb - sa;
			return (a.name ?? '').localeCompare(b.name ?? '');
		});
	const { items, pagination } = paginate(matched, page, limit);
	return {
		companies: items.map((c) => ({
			...c,
			involvement_types: c.involvement_types ?? []
		})),
		pagination
	};
}

export function searchSuggestions(query: string, limit = 10) {
	const cleaned = query.trim().toLowerCase();
	if (cleaned.length < 2) return [];
	const matches: Company[] = [];
	for (const c of companies) {
		if ((c.name ?? '').toLowerCase().includes(cleaned)) {
			matches.push(c);
			if (matches.length >= limit * 4) break;
		}
	}
	matches.sort((a, b) => {
		const sa = a.confidence_score ?? -Infinity;
		const sb = b.confidence_score ?? -Infinity;
		if (sa !== sb) return sb - sa;
		return (a.name ?? '').localeCompare(b.name ?? '');
	});
	return matches.slice(0, limit).map((c) => ({ id: c.id, name: c.name }));
}

let cachedStats: ReturnType<typeof computeStats> | null = null;

function computeStats() {
	const involvement = new Map<string, number>();
	const countries = new Map<string, number>();
	const industries = new Map<string, number>();
	const sourceSet = new Set<string>();

	for (const c of companies) {
		for (const t of c.involvement_types ?? []) {
			if (!t) continue;
			involvement.set(t, (involvement.get(t) ?? 0) + 1);
		}
		if (c.country_hq) {
			countries.set(c.country_hq, (countries.get(c.country_hq) ?? 0) + 1);
		}
		if (c.industry) {
			industries.set(c.industry, (industries.get(c.industry) ?? 0) + 1);
		}
		for (const s of c.data_sources ?? []) {
			if (s) sourceSet.add(s);
		}
	}

	const toSorted = (m: Map<string, number>, key: string) =>
		Array.from(m.entries())
			.sort((a, b) => b[1] - a[1])
			.map(([k, count]) => ({ [key]: k, count }));

	return {
		totalCompanies: companies.length,
		totalSources: sourceSet.size,
		involvementTypes: toSorted(involvement, 'involvement_type'),
		topCountries: toSorted(countries, 'country_hq').slice(0, 10),
		topIndustries: toSorted(industries, 'industry').slice(0, 10)
	};
}

export function getStats() {
	if (!cachedStats) cachedStats = computeStats();
	return cachedStats;
}
