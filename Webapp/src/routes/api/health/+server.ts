import { json } from '@sveltejs/kit';
import { getStats } from '$lib/server/data';

export async function GET() {
	const stats = getStats();
	return json({
		status: 'healthy',
		totalCompanies: stats.totalCompanies,
		timestamp: new Date().toISOString()
	});
}
