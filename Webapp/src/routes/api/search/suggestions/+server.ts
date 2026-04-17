import { json } from '@sveltejs/kit';
import { searchSuggestions } from '$lib/server/data';

export async function GET({ url }) {
	const search = url.searchParams.get('q') || '';
	return json(searchSuggestions(search));
}
