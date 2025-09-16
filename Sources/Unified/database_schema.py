#!/usr/bin/env python3
"""
Database Schema Creation for BDS Unified Data

This script creates the necessary PostgreSQL tables to store unified BDS data.
"""

import os
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def create_database_schema():
    """Create the database schema for unified BDS data"""

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not set")

    try:
        # Connect to the database
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()

        logger.info("Connected to Neon database")

        # Drop existing tables if they exist (for development)
        logger.info("Dropping existing tables if they exist...")
        cursor.execute("DROP TABLE IF EXISTS company_stock_symbols CASCADE")
        cursor.execute("DROP TABLE IF EXISTS company_sources CASCADE")
        cursor.execute("DROP TABLE IF EXISTS company_reasons CASCADE")
        cursor.execute("DROP TABLE IF EXISTS company_boycott_actions CASCADE")
        cursor.execute("DROP TABLE IF EXISTS company_alternatives CASCADE")
        cursor.execute("DROP TABLE IF EXISTS company_campaigns CASCADE")
        cursor.execute("DROP TABLE IF EXISTS company_sectors CASCADE")
        cursor.execute("DROP TABLE IF EXISTS company_involvement_types CASCADE")
        cursor.execute("DROP TABLE IF EXISTS companies CASCADE")

        # Create companies table
        logger.info("Creating companies table...")
        cursor.execute("""
            CREATE TABLE companies (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(500) NOT NULL,
                standard_name VARCHAR(500),
                parent_company VARCHAR(500),
                country_hq VARCHAR(100),
                industry VARCHAR(200),
                description TEXT,
                booth_number VARCHAR(50),
                divestment_priority VARCHAR(20),
                confidence_score DECIMAL(3,2),
                verification_status VARCHAR(20),
                involvement_details JSONB,
                last_updated TIMESTAMP WITH TIME ZONE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX idx_companies_name ON companies(name)")
        cursor.execute("CREATE INDEX idx_companies_country ON companies(country_hq)")
        cursor.execute("CREATE INDEX idx_companies_industry ON companies(industry)")
        cursor.execute("CREATE INDEX idx_companies_confidence ON companies(confidence_score)")

        # Create stock symbols table
        logger.info("Creating company_stock_symbols table...")
        cursor.execute("""
            CREATE TABLE company_stock_symbols (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                symbol VARCHAR(20) NOT NULL,
                exchange VARCHAR(200) NOT NULL,
                isin VARCHAR(12)
            )
        """)
        cursor.execute("CREATE INDEX idx_stock_symbols_company ON company_stock_symbols(company_id)")
        cursor.execute("CREATE INDEX idx_stock_symbols_symbol ON company_stock_symbols(symbol)")

        # Create sources table
        logger.info("Creating company_sources table...")
        cursor.execute("""
            CREATE TABLE company_sources (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                source_url TEXT NOT NULL,
                source_type VARCHAR(50) DEFAULT 'evidence'
            )
        """)
        cursor.execute("CREATE INDEX idx_sources_company ON company_sources(company_id)")

        # Create data sources tracking table
        logger.info("Creating company_data_sources table...")
        cursor.execute("""
            CREATE TABLE company_data_sources (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                data_source VARCHAR(100) NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_data_sources_company ON company_data_sources(company_id)")

        # Create reasons table
        logger.info("Creating company_reasons table...")
        cursor.execute("""
            CREATE TABLE company_reasons (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                summary TEXT NOT NULL,
                details TEXT,
                source_url TEXT,
                date_added DATE
            )
        """)
        cursor.execute("CREATE INDEX idx_reasons_company ON company_reasons(company_id)")

        # Create boycott actions table
        logger.info("Creating company_boycott_actions table...")
        cursor.execute("""
            CREATE TABLE company_boycott_actions (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                action TEXT NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_boycott_actions_company ON company_boycott_actions(company_id)")

        # Create alternatives table
        logger.info("Creating company_alternatives table...")
        cursor.execute("""
            CREATE TABLE company_alternatives (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                alternative VARCHAR(500) NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_alternatives_company ON company_alternatives(company_id)")

        # Create campaigns table
        logger.info("Creating company_campaigns table...")
        cursor.execute("""
            CREATE TABLE company_campaigns (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                campaign_name VARCHAR(500) NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_campaigns_company ON company_campaigns(company_id)")

        # Create sectors table
        logger.info("Creating company_sectors table...")
        cursor.execute("""
            CREATE TABLE company_sectors (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                sector VARCHAR(200) NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_sectors_company ON company_sectors(company_id)")

        # Create involvement types table
        logger.info("Creating company_involvement_types table...")
        cursor.execute("""
            CREATE TABLE company_involvement_types (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                involvement_type VARCHAR(100) NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_involvement_types_company ON company_involvement_types(company_id)")

        # Create aliases table
        logger.info("Creating company_aliases table...")
        cursor.execute("""
            CREATE TABLE company_aliases (
                id SERIAL PRIMARY KEY,
                company_id VARCHAR(255) REFERENCES companies(id) ON DELETE CASCADE,
                alias VARCHAR(500) NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX idx_aliases_company ON company_aliases(company_id)")

        # Create a view for easy querying
        logger.info("Creating companies_full_view...")
        cursor.execute("""
            CREATE OR REPLACE VIEW companies_full_view AS
            SELECT
                c.*,
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
                    json_agg(DISTINCT cba.action) FILTER (WHERE cba.action IS NOT NULL),
                    '[]'::json
                ) as boycott_actions,
                COALESCE(
                    json_agg(DISTINCT ca.alternative) FILTER (WHERE ca.alternative IS NOT NULL),
                    '[]'::json
                ) as alternatives,
                COALESCE(
                    json_agg(DISTINCT cc.campaign_name) FILTER (WHERE cc.campaign_name IS NOT NULL),
                    '[]'::json
                ) as campaigns,
                COALESCE(
                    json_agg(DISTINCT csec.sector) FILTER (WHERE csec.sector IS NOT NULL),
                    '[]'::json
                ) as sectors,
                COALESCE(
                    json_agg(DISTINCT cit.involvement_type) FILTER (WHERE cit.involvement_type IS NOT NULL),
                    '[]'::json
                ) as involvement_types,
                COALESCE(
                    json_agg(DISTINCT cal.alias) FILTER (WHERE cal.alias IS NOT NULL),
                    '[]'::json
                ) as aliases
            FROM companies c
            LEFT JOIN company_stock_symbols css ON c.id = css.company_id
            LEFT JOIN company_sources cs ON c.id = cs.company_id
            LEFT JOIN company_data_sources cds ON c.id = cds.company_id
            LEFT JOIN company_reasons cr ON c.id = cr.company_id
            LEFT JOIN company_boycott_actions cba ON c.id = cba.company_id
            LEFT JOIN company_alternatives ca ON c.id = ca.company_id
            LEFT JOIN company_campaigns cc ON c.id = cc.company_id
            LEFT JOIN company_sectors csec ON c.id = csec.company_id
            LEFT JOIN company_involvement_types cit ON c.id = cit.company_id
            LEFT JOIN company_aliases cal ON c.id = cal.company_id
            GROUP BY c.id
        """)

        logger.info("Database schema created successfully!")

        # Test the connection and show table info
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        logger.info(f"Created {len(tables)} tables: {[t[0] for t in tables]}")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error creating database schema: {e}")
        raise


if __name__ == "__main__":
    create_database_schema()