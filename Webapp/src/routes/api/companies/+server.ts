import { json } from '@sveltejs/kit';
import { searchCompanies } from '$lib/server/data';

export async function GET({ url }) {
	const page = parseInt(url.searchParams.get('page') || '1');
	const limit = parseInt(url.searchParams.get('limit') || '20');
	const search = url.searchParams.get('search') || '';

	return json(searchCompanies({ search, page, limit }));
}
