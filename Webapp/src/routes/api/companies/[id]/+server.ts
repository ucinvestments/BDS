import { json } from '@sveltejs/kit';
import { getCompanyById } from '$lib/server/data';

export async function GET({ params }) {
	const company = getCompanyById(params.id);
	if (!company) return json({ error: 'Company not found' }, { status: 404 });
	return json(company);
}
