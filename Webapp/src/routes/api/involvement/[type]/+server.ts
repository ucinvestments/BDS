import { json } from '@sveltejs/kit';
import { findByInvolvement } from '$lib/server/data';

export async function GET({ params, url }) {
	const page = parseInt(url.searchParams.get('page') || '1');
	const limit = parseInt(url.searchParams.get('limit') || '20');
	return json(findByInvolvement(params.type, page, limit));
}
