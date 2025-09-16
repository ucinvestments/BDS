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
    await pool.query('SELECT 1');
    return json({ status: 'healthy', timestamp: new Date().toISOString() });
  } catch (error) {
    return json({ status: 'unhealthy', error: error.message }, { status: 500 });
  }
}