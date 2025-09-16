import { json } from '@sveltejs/kit';
import pkg from 'pg';
import { DATABASE_URL } from '$env/static/private';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

// Helper function for semantic search using PostgreSQL full-text search
function buildSearchQuery(searchTerm: string) {
  if (!searchTerm || searchTerm.trim() === '') {
    return {
      whereClause: '',
      params: []
    };
  }

  // Clean and prepare search term for full-text search
  const cleanTerm = searchTerm.trim().toLowerCase();
  const tsQuery = cleanTerm.split(/\s+/).join(' & ');

  return {
    whereClause: `
      WHERE (
        to_tsvector('english', c.name) @@ to_tsquery('english', $1)
        OR to_tsvector('english', COALESCE(c.description, '')) @@ to_tsquery('english', $1)
        OR to_tsvector('english', COALESCE(c.industry, '')) @@ to_tsquery('english', $1)
        OR c.name ILIKE $2
        OR COALESCE(c.description, '') ILIKE $2
        OR EXISTS (
          SELECT 1 FROM company_involvement_types cit
          WHERE cit.company_id = c.id AND cit.involvement_type ILIKE $2
        )
        OR EXISTS (
          SELECT 1 FROM company_sectors cs
          WHERE cs.company_id = c.id AND cs.sector ILIKE $2
        )
        OR EXISTS (
          SELECT 1 FROM company_reasons cr
          WHERE cr.company_id = c.id
          AND (cr.summary ILIKE $2 OR COALESCE(cr.details, '') ILIKE $2)
        )
      )
    `,
    params: [tsQuery, `%${cleanTerm}%`]
  };
}

export async function GET({ url }) {
  try {
    const page = parseInt(url.searchParams.get('page') || '1');
    const limit = parseInt(url.searchParams.get('limit') || '20');
    const search = url.searchParams.get('search') || '';
    const offset = (page - 1) * limit;

    const { whereClause, params } = buildSearchQuery(search);

    const query = `
      SELECT
        c.id,
        c.name,
        c.description,
        c.industry,
        c.country_hq,
        c.parent_company,
        COALESCE(
          json_agg(
            DISTINCT jsonb_build_object(
              'symbol', css.symbol,
              'exchange', css.exchange,
              'isin', css.isin
            )
          ) FILTER (WHERE css.symbol IS NOT NULL),
          '[]'::json
        ) as stock_symbols,
        COALESCE(
          json_agg(DISTINCT cs.source_url) FILTER (WHERE cs.source_url IS NOT NULL),
          '[]'::json
        ) as sources,
        COALESCE(
          json_agg(DISTINCT cds.data_source) FILTER (WHERE cds.data_source IS NOT NULL),
          '[]'::json
        ) as data_sources,
        COALESCE(
          json_agg(DISTINCT cit.involvement_type) FILTER (WHERE cit.involvement_type IS NOT NULL),
          '[]'::json
        ) as involvement_types,
        COALESCE(
          json_agg(DISTINCT csec.sector) FILTER (WHERE csec.sector IS NOT NULL),
          '[]'::json
        ) as sectors,
        COALESCE(
          json_agg(DISTINCT cba.action) FILTER (WHERE cba.action IS NOT NULL),
          '[]'::json
        ) as boycott_actions,
        COALESCE(
          json_agg(DISTINCT ca.alternative) FILTER (WHERE ca.alternative IS NOT NULL),
          '[]'::json
        ) as alternatives
      FROM companies c
      LEFT JOIN company_stock_symbols css ON c.id = css.company_id
      LEFT JOIN company_sources cs ON c.id = cs.company_id
      LEFT JOIN company_data_sources cds ON c.id = cds.company_id
      LEFT JOIN company_involvement_types cit ON c.id = cit.company_id
      LEFT JOIN company_sectors csec ON c.id = csec.company_id
      LEFT JOIN company_boycott_actions cba ON c.id = cba.company_id
      LEFT JOIN company_alternatives ca ON c.id = ca.company_id
      ${whereClause}
      GROUP BY c.id
      ORDER BY c.name
      LIMIT $${params.length + 1} OFFSET $${params.length + 2}
    `;

    const countQuery = `
      SELECT COUNT(DISTINCT c.id) as total
      FROM companies c
      ${whereClause}
    `;

    const [companiesResult, countResult] = await Promise.all([
      pool.query(query, [...params, limit, offset]),
      pool.query(countQuery, params)
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
    console.error('Error fetching companies:', error);
    return json({ error: 'Internal server error' }, { status: 500 });
  }
}