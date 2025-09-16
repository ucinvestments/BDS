import { json } from '@sveltejs/kit';
import pkg from 'pg';
import { DATABASE_URL } from '$env/static/private';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

export async function GET({ params }) {
  try {
    const { id } = params;

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
          json_agg(
            DISTINCT jsonb_build_object(
              'summary', cr.summary,
              'details', cr.details,
              'source', cr.source_url,
              'date_added', cr.date_added
            )
          ) FILTER (WHERE cr.summary IS NOT NULL),
          '[]'::json
        ) as reasons,
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
        ) as alternatives,
        COALESCE(
          json_agg(DISTINCT cal.alias) FILTER (WHERE cal.alias IS NOT NULL),
          '[]'::json
        ) as aliases
      FROM companies c
      LEFT JOIN company_stock_symbols css ON c.id = css.company_id
      LEFT JOIN company_sources cs ON c.id = cs.company_id
      LEFT JOIN company_data_sources cds ON c.id = cds.company_id
      LEFT JOIN company_reasons cr ON c.id = cr.company_id
      LEFT JOIN company_involvement_types cit ON c.id = cit.company_id
      LEFT JOIN company_sectors csec ON c.id = csec.company_id
      LEFT JOIN company_boycott_actions cba ON c.id = cba.company_id
      LEFT JOIN company_alternatives ca ON c.id = ca.company_id
      LEFT JOIN company_aliases cal ON c.id = cal.company_id
      WHERE c.id = $1
      GROUP BY c.id
    `;

    const result = await pool.query(query, [id]);

    if (result.rows.length === 0) {
      return json({ error: 'Company not found' }, { status: 404 });
    }

    return json(result.rows[0]);
  } catch (error) {
    console.error('Error fetching company:', error);
    return json({ error: 'Internal server error' }, { status: 500 });
  }
}