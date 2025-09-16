import { json } from '@sveltejs/kit';
import pkg from 'pg';
import { DATABASE_URL } from '$env/static/private';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

export async function GET({ url }) {
  try {
    const search = url.searchParams.get('q') || '';

    if (search.length < 2) {
      return json([]);
    }

    const query = `
      SELECT DISTINCT c.name, c.id
      FROM companies c
      WHERE c.name ILIKE $1
      ORDER BY c.confidence_score DESC NULLS LAST, c.name
      LIMIT 10
    `;

    const result = await pool.query(query, [`%${search}%`]);

    return json(result.rows);
  } catch (error) {
    console.error('Error fetching suggestions:', error);
    return json({ error: 'Internal server error' }, { status: 500 });
  }
}