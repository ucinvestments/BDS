import { json } from '@sveltejs/kit';
import pkg from 'pg';
import { DATABASE_URL } from '$env/static/private';
const { Pool } = pkg;

const pool = new Pool({
  connectionString: DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false
});

export async function GET() {
  try {
    const queries = [
      'SELECT COUNT(*) as total_companies FROM companies',
      'SELECT COUNT(DISTINCT data_source) as total_sources FROM company_data_sources',
      'SELECT involvement_type, COUNT(*) as count FROM company_involvement_types GROUP BY involvement_type ORDER BY count DESC',
      'SELECT country_hq, COUNT(*) as count FROM companies WHERE country_hq IS NOT NULL GROUP BY country_hq ORDER BY count DESC LIMIT 10',
      'SELECT industry, COUNT(*) as count FROM companies WHERE industry IS NOT NULL GROUP BY industry ORDER BY count DESC LIMIT 10'
    ];

    const results = await Promise.all(queries.map(query => pool.query(query)));

    return json({
      totalCompanies: parseInt(results[0].rows[0].total_companies),
      totalSources: parseInt(results[1].rows[0].total_sources),
      involvementTypes: results[2].rows,
      topCountries: results[3].rows,
      topIndustries: results[4].rows
    });
  } catch (error) {
    console.error('Error fetching statistics:', error);
    return json({ error: 'Internal server error' }, { status: 500 });
  }
}