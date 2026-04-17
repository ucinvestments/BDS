import { json } from '@sveltejs/kit';
import { getStats } from '$lib/server/data';

export async function GET() {
	return json(getStats());
}
