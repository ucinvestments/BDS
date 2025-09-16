import { json } from '@sveltejs/kit';
import pkg from 'pg';
import { DATABASE_URL } from '$env/static/private';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

export async function GET({ params, url }) {
  try {
    const { type } = params;
    const page = parseInt(url.searchParams.get('page') || '1');
    const limit = parseInt(url.searchParams.get('limit') || '20');
    const offset = (page - 1) * limit;

    const query = `
      SELECT
        c.*,
        COALESCE(
          json_agg(DISTINCT cit.involvement_type) FILTER (WHERE cit.involvement_type IS NOT NULL),
          '[]'::json
        ) as involvement_types
      FROM companies c
      INNER JOIN company_involvement_types cit ON c.id = cit.company_id
      WHERE cit.involvement_type = $1
      GROUP BY c.id
      ORDER BY c.confidence_score DESC NULLS LAST, c.name
      LIMIT $2 OFFSET $3
    `;

    const countQuery = `
      SELECT COUNT(DISTINCT c.id) as total
      FROM companies c
      INNER JOIN company_involvement_types cit ON c.id = cit.company_id
      WHERE cit.involvement_type = $1
    `;

    const [companiesResult, countResult] = await Promise.all([
      pool.query(query, [type, limit, offset]),
      pool.query(countQuery, [type])
    ]);

    const total = parseInt(countResult.rows[0].total);
    const totalPages = Math.ceil(total / limit);

    return json({
      companies: companiesResult.rows,
      pagination: {
        page,
        limit,
        total,
        totalPages,
        hasNext: page < totalPages,
        hasPrev: page > 1
      }
    });
  } catch (error) {
    console.error('Error fetching companies by involvement:', error);
    return json({ error: 'Internal server error' }, { status: 500 });
  }
}