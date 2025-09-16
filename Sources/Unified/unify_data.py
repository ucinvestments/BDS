#!/usr/bin/env python3
"""
BDS Data Unification Script

This script combines data from multiple BDS sources into a unified format
according to the defined schema.
"""

import json
import csv
import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import hashlib
import re
from collections import defaultdict
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schema_validator import BDSSchemaValidator

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataUnifier:
    """Unifies BDS data from multiple sources into a single schema"""

    def __init__(self, output_dir: str = "/app/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.validator = BDSSchemaValidator()
        self.unified_data = {}
        self.stats = {
            'total_records': 0,
            'sources_processed': [],
            'duplicates_merged': 0,
            'validation_errors': 0,
            'database_inserts': 0,
            'database_errors': 0
        }

        # Database connection
        self.database_url = os.getenv('DATABASE_URL')
        self.db_conn = None

    def connect_to_database(self):
        """Connect to the PostgreSQL database"""
        if not self.database_url:
            logger.warning("DATABASE_URL not set, skipping database operations")
            return False

        try:
            self.db_conn = psycopg2.connect(self.database_url)
            logger.info("Connected to Neon database")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False

    def close_database_connection(self):
        """Close database connection"""
        if self.db_conn:
            self.db_conn.close()
            logger.info("Database connection closed")

    def insert_company_to_database(self, record: Dict[str, Any]):
        """Insert a company record into the database"""
        if not self.db_conn:
            return

        try:
            cursor = self.db_conn.cursor()

            # Insert main company record
            cursor.execute("""
                INSERT INTO companies (
                    id, name, standard_name, parent_company, country_hq,
                    industry, description, booth_number, divestment_priority,
                    confidence_score, verification_status, involvement_details,
                    last_updated
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    standard_name = EXCLUDED.standard_name,
                    parent_company = EXCLUDED.parent_company,
                    country_hq = EXCLUDED.country_hq,
                    industry = EXCLUDED.industry,
                    description = EXCLUDED.description,
                    booth_number = EXCLUDED.booth_number,
                    divestment_priority = EXCLUDED.divestment_priority,
                    confidence_score = EXCLUDED.confidence_score,
                    verification_status = EXCLUDED.verification_status,
                    involvement_details = EXCLUDED.involvement_details,
                    last_updated = EXCLUDED.last_updated
            """, (
                record['id'],
                record['name'],
                record.get('standard_name'),
                record.get('parent_company'),
                record.get('country_hq'),
                record.get('industry'),
                record.get('description'),
                record.get('booth_number'),
                record.get('divestment_priority'),
                record.get('confidence_score'),
                record.get('verification_status'),
                json.dumps(record.get('involvement_details', {})),
                record['last_updated']
            ))

            # Clear existing related records to avoid duplicates
            cursor.execute("DELETE FROM company_stock_symbols WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_sources WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_data_sources WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_reasons WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_boycott_actions WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_alternatives WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_campaigns WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_sectors WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_involvement_types WHERE company_id = %s", (record['id'],))
            cursor.execute("DELETE FROM company_aliases WHERE company_id = %s", (record['id'],))

            # Insert stock symbols
            for symbol_data in record.get('stock_symbols', []):
                cursor.execute("""
                    INSERT INTO company_stock_symbols (company_id, symbol, exchange, isin)
                    VALUES (%s, %s, %s, %s)
                """, (
                    record['id'],
                    symbol_data['symbol'],
                    symbol_data['exchange'],
                    symbol_data.get('isin')
                ))

            # Insert sources
            for source in record.get('sources', []):
                if source and source.strip():
                    cursor.execute("""
                        INSERT INTO company_sources (company_id, source_url)
                        VALUES (%s, %s)
                    """, (record['id'], source.strip()))

            # Insert data sources
            for data_source in record.get('data_sources', []):
                cursor.execute("""
                    INSERT INTO company_data_sources (company_id, data_source)
                    VALUES (%s, %s)
                """, (record['id'], data_source))

            # Insert reasons
            for reason in record.get('reasons', []):
                cursor.execute("""
                    INSERT INTO company_reasons (company_id, summary, details, source_url, date_added)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    record['id'],
                    reason['summary'],
                    reason.get('details'),
                    reason.get('source'),
                    reason.get('date_added')
                ))

            # Insert boycott actions
            for action in record.get('boycott_actions', []):
                cursor.execute("""
                    INSERT INTO company_boycott_actions (company_id, action)
                    VALUES (%s, %s)
                """, (record['id'], action))

            # Insert alternatives
            for alternative in record.get('alternatives', []):
                cursor.execute("""
                    INSERT INTO company_alternatives (company_id, alternative)
                    VALUES (%s, %s)
                """, (record['id'], alternative))

            # Insert campaigns
            for campaign in record.get('campaigns', []):
                cursor.execute("""
                    INSERT INTO company_campaigns (company_id, campaign_name)
                    VALUES (%s, %s)
                """, (record['id'], campaign))

            # Insert sectors
            for sector in record.get('sectors', []):
                cursor.execute("""
                    INSERT INTO company_sectors (company_id, sector)
                    VALUES (%s, %s)
                """, (record['id'], sector))

            # Insert involvement types
            for involvement_type in record.get('involvement_types', []):
                cursor.execute("""
                    INSERT INTO company_involvement_types (company_id, involvement_type)
                    VALUES (%s, %s)
                """, (record['id'], involvement_type))

            # Insert aliases
            for alias in record.get('aliases', []):
                cursor.execute("""
                    INSERT INTO company_aliases (company_id, alias)
                    VALUES (%s, %s)
                """, (record['id'], alias))

            cursor.close()
            self.stats['database_inserts'] += 1

        except Exception as e:
            logger.error(f"Error inserting company {record['name']} to database: {e}")
            self.stats['database_errors'] += 1

    def normalize_company_name(self, name: str) -> str:
        """Normalize company name for matching"""
        if not name:
            return ""

        # Remove common suffixes
        suffixes = [
            r'\s+LLC$', r'\s+Inc\.?$', r'\s+Ltd\.?$', r'\s+Corporation$',
            r'\s+Corp\.?$', r'\s+Company$', r'\s+Co\.?$', r'\s+Group$',
            r'\s+plc$', r'\s+PLC$', r'\s+SE$', r'\s+SA$', r'\s+AG$',
            r'\s+GmbH$', r'\s+NV$', r'\s+BV$', r'\s+AB$', r'\s+AS$'
        ]

        normalized = name.strip()
        for suffix in suffixes:
            normalized = re.sub(suffix, '', normalized, flags=re.IGNORECASE)

        # Convert to lowercase and remove special characters for matching
        normalized = re.sub(r'[^\w\s]', '', normalized.lower())
        normalized = ' '.join(normalized.split())  # Normalize whitespace

        return normalized

    def generate_id(self, name: str) -> str:
        """Generate a stable ID for a company"""
        normalized = self.normalize_company_name(name)
        # Create a short hash for the ID
        hash_obj = hashlib.md5(normalized.encode())
        short_hash = hash_obj.hexdigest()[:8]
        # Create ID from normalized name (alphanumeric only)
        clean_name = re.sub(r'[^a-z0-9]', '_', normalized)[:20]
        return f"comp_{clean_name}_{short_hash}"

    def load_bds_coalition_csv(self, file_path: str) -> List[Dict]:
        """Load BDS Coalition CSV data"""
        records = []

        if not os.path.exists(file_path):
            logger.warning(f"BDS Coalition file not found: {file_path}")
            return records

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    record = {
                        'id': self.generate_id(row.get('Name', '')),
                        'name': row.get('Name', '').strip(),
                        'parent_company': row.get('Parent Company', '').strip() or None,
                        'country_hq': row.get('Country', '').strip() or None,
                        'description': row.get('Description', '').strip() or None,
                        'reasons': [{
                            'summary': row.get('Description', '').strip()[:200] if row.get('Description') else 'Listed in BDS Coalition database',
                            'details': row.get('Description', '').strip() or None,
                            'source': row.get('Sources / Links', '').strip() or None
                        }],
                        'sources': [s.strip() for s in row.get('Sources / Links', '').split(',') if s.strip()],
                        'data_sources': ['bdscoalition.ca'],
                        'last_updated': datetime.now().isoformat()
                    }
                    records.append(record)

        except Exception as e:
            logger.error(f"Error loading BDS Coalition CSV: {e}")

        logger.info(f"Loaded {len(records)} records from BDS Coalition")
        return records

    def load_afsc_investigate_csv(self, file_path: str) -> List[Dict]:
        """Load AFSC Investigate CSV data"""
        records = []

        if not os.path.exists(file_path):
            logger.warning(f"AFSC file not found: {file_path}")
            return records

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Parse involvement details
                    involvement_details = {}
                    involvement_types = []

                    if row.get('Prisons') == '1':
                        involvement_details['prisons'] = True
                        involvement_types.append('prison_industry')

                    if row.get('Occupations') == '1':
                        involvement_details['occupations'] = True
                        involvement_types.append('occupation')

                    if row.get('Borders') == '1':
                        involvement_details['borders'] = True
                        involvement_types.append('border_security')

                    # Check summary for additional involvement types
                    summary = row.get('Summary', '').lower()
                    if 'settlement' in summary:
                        involvement_details['settlements'] = True
                        involvement_types.append('settlements')
                    if 'military' in summary or 'weapon' in summary or 'defense' in summary:
                        involvement_details['military'] = True
                        involvement_types.append('military_support')

                    record = {
                        'id': self.generate_id(row.get('Company Short Name', '')),
                        'name': row.get('Company Short Name', '').strip(),
                        'standard_name': row.get('Company Standard Name', '').strip() or None,
                        'country_hq': row.get('Country of HQ', '').strip() or None,
                        'industry': row.get('Industry', '').strip() or None,
                        'description': row.get('Summary', '').strip() or None,
                        'stock_symbols': [],
                        'involvement_types': involvement_types,
                        'involvement_details': involvement_details,
                        'divestment_priority': 'shortlist' if row.get('Divestment Shortlist') == '1' else None,
                        'reasons': [{
                            'summary': row.get('Summary', '').strip()[:200] if row.get('Summary') else 'Listed in AFSC Investigate database',
                            'details': row.get('Summary', '').strip() or None,
                            'source': row.get('Link', '').strip() or None
                        }],
                        'sources': [row.get('Link', '').strip()] if row.get('Link') else [],
                        'data_sources': ['investigate.afsc.org'],
                        'last_updated': datetime.now().isoformat()
                    }

                    # Add stock information if available
                    if row.get('Primary Symbol'):
                        record['stock_symbols'].append({
                            'symbol': row.get('Primary Symbol', '').strip(),
                            'exchange': row.get('Primary Exchange Name', '').strip() or row.get('Primary Exchange Short', '').strip(),
                            'isin': row.get('Primary ISIN', '').strip() or None
                        })

                    records.append(record)

        except Exception as e:
            logger.error(f"Error loading AFSC CSV: {e}")

        logger.info(f"Loaded {len(records)} records from AFSC Investigate")
        return records

    def load_boycott_thewitness_json(self, file_path: str) -> List[Dict]:
        """Load Boycott.thewitness JSON data"""
        records = []

        if not os.path.exists(file_path):
            logger.warning(f"Boycott.thewitness file not found: {file_path}")
            return records

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                brands = data.get('sample_enhanced_brands', [])
                for brand in brands:
                    # Map categories to involvement types
                    involvement_types = []
                    categories = brand.get('categories', [])
                    reason_text = brand.get('reason', '').lower()

                    if 'military' in reason_text or 'weapon' in reason_text:
                        involvement_types.append('military_support')
                    if 'surveillance' in reason_text:
                        involvement_types.append('surveillance')
                    if 'settlement' in reason_text:
                        involvement_types.append('settlements')
                    if 'occupation' in reason_text:
                        involvement_types.append('occupation')

                    record = {
                        'id': self.generate_id(brand.get('name', '')),
                        'name': brand.get('name', '').strip(),
                        'description': brand.get('description', '').strip() or None,
                        'sectors': categories,
                        'involvement_types': involvement_types,
                        'reasons': [{
                            'summary': brand.get('reason', '').strip()[:200] if brand.get('reason') else 'Listed in boycott database',
                            'details': brand.get('reason', '').strip() or None,
                            'source': brand.get('source', '').strip() or None
                        }],
                        'sources': [brand.get('source', '').strip()] if brand.get('source') else [],
                        'boycott_actions': brand.get('how_to_boycott', []),
                        'alternatives': brand.get('alternatives', []),
                        'data_sources': ['boycott.thewitness'],
                        'last_updated': datetime.now().isoformat()
                    }
                    records.append(record)

        except Exception as e:
            logger.error(f"Error loading Boycott.thewitness JSON: {e}")

        logger.info(f"Loaded {len(records)} records from Boycott.thewitness")
        return records

    def load_who_profits_json(self, file_path: str) -> List[Dict]:
        """Load Who Profits search results JSON"""
        records = []

        if not os.path.exists(file_path):
            logger.warning(f"Who Profits file not found: {file_path}")
            return records

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                results = data.get('results', {})
                for booth, company_data in results.items():
                    if company_data.get('found'):
                        for match in company_data.get('matches', []):
                            # Determine involvement types from the involvement field
                            involvement_types = []
                            involvement_text = match.get('involvement', '').lower()

                            if 'settlement' in involvement_text:
                                involvement_types.append('settlements')
                            if 'military' in involvement_text or 'defense' in involvement_text:
                                involvement_types.append('military_support')
                            if 'occupation' in involvement_text:
                                involvement_types.append('occupation')

                            record = {
                                'id': self.generate_id(match.get('company_name', '')),
                                'name': match.get('company_name', '').strip(),
                                'country_hq': match.get('headquarters', '').strip() or None,
                                'booth_number': booth,
                                'involvement_types': involvement_types,
                                'reasons': [{
                                    'summary': f"Found in Who Profits database: {match.get('involvement', 'Listed')}",
                                    'details': match.get('involvement', '').strip() or None,
                                    'source': 'https://www.whoprofits.org'
                                }],
                                'sources': ['https://www.whoprofits.org'],
                                'data_sources': ['whoprofits.org'],
                                'last_updated': datetime.now().isoformat()
                            }
                            records.append(record)

        except Exception as e:
            logger.error(f"Error loading Who Profits JSON: {e}")

        logger.info(f"Loaded {len(records)} records from Who Profits")
        return records

    def merge_records(self, existing: Dict, new: Dict) -> Dict:
        """Merge two records for the same company"""
        # Start with existing record
        merged = existing.copy()

        # Update basic fields if new has better data
        if new.get('standard_name') and not merged.get('standard_name'):
            merged['standard_name'] = new['standard_name']

        if new.get('parent_company') and not merged.get('parent_company'):
            merged['parent_company'] = new['parent_company']

        if new.get('country_hq') and not merged.get('country_hq'):
            merged['country_hq'] = new['country_hq']

        if new.get('industry') and not merged.get('industry'):
            merged['industry'] = new['industry']

        if new.get('description') and len(new['description']) > len(merged.get('description', '')):
            merged['description'] = new['description']

        # Merge arrays
        for field in ['aliases', 'sectors', 'involvement_types', 'sources',
                     'evidence_links', 'boycott_actions', 'alternatives',
                     'campaigns', 'data_sources']:
            if field in new:
                if field not in merged:
                    merged[field] = []
                merged[field] = list(set(merged[field] + new[field]))

        # Merge stock symbols
        if 'stock_symbols' in new:
            if 'stock_symbols' not in merged:
                merged['stock_symbols'] = []
            # Avoid duplicate symbols
            existing_symbols = {s['symbol'] for s in merged['stock_symbols']}
            for symbol in new['stock_symbols']:
                if symbol['symbol'] not in existing_symbols:
                    merged['stock_symbols'].append(symbol)

        # Merge involvement details
        if 'involvement_details' in new:
            if 'involvement_details' not in merged:
                merged['involvement_details'] = {}
            merged['involvement_details'].update(new['involvement_details'])

        # Append reasons
        if 'reasons' in new:
            if 'reasons' not in merged:
                merged['reasons'] = []
            merged['reasons'].extend(new['reasons'])

        # Update priority if new has higher priority
        if new.get('divestment_priority') == 'shortlist':
            merged['divestment_priority'] = 'shortlist'

        # Update booth number if available
        if new.get('booth_number'):
            merged['booth_number'] = new['booth_number']

        # Calculate confidence score based on number of sources
        merged['confidence_score'] = min(1.0, len(merged.get('data_sources', [])) * 0.25)

        # Update timestamp
        merged['last_updated'] = datetime.now().isoformat()

        self.stats['duplicates_merged'] += 1

        return merged

    def unify_all_sources(self):
        """Load and unify data from all available sources"""
        # Check if running in Docker (Sources mounted at /app/Sources)
        if os.path.exists('/app/Sources'):
            base_dir = Path('/app/Sources')
        else:
            # Running locally
            base_dir = Path(__file__).parent.parent

        # Load BDS Coalition data
        bds_file = base_dir / "bdscoalition.ca" / "BDS Shame List (20AUG2025).csv"
        bds_records = self.load_bds_coalition_csv(str(bds_file))
        self._add_records(bds_records)

        # Load AFSC Investigate data
        afsc_file = base_dir / "investigate.afsc.org" / "investigate-dataset-july-2025.csv"
        afsc_records = self.load_afsc_investigate_csv(str(afsc_file))
        self._add_records(afsc_records)

        # Load Boycott.thewitness data
        boycott_file = base_dir / "boycott.thewitness" / "sample_output.json"
        boycott_records = self.load_boycott_thewitness_json(str(boycott_file))
        self._add_records(boycott_records)

        # Load Who Profits data (if exists)
        who_profits_file = base_dir / "dontbuyintooccupation.org" / "output" / "who_profits_results_latest.json"
        if who_profits_file.exists():
            who_profits_records = self.load_who_profits_json(str(who_profits_file))
            self._add_records(who_profits_records)

    def _add_records(self, records: List[Dict]):
        """Add records to unified data, merging duplicates"""
        logger.info(f"Processing {len(records)} records...")
        for i, record in enumerate(records):
            if i % 100 == 0 and i > 0:
                logger.info(f"  Processed {i}/{len(records)} records...")
            # Normalize the company name for matching
            normalized_name = self.normalize_company_name(record['name'])

            # Check if we already have this company
            found = False
            for existing_id, existing_record in self.unified_data.items():
                existing_normalized = self.normalize_company_name(existing_record['name'])

                # Check for name match or same ID
                if existing_normalized == normalized_name or existing_id == record['id']:
                    # Merge the records
                    self.unified_data[existing_id] = self.merge_records(existing_record, record)
                    found = True
                    break

            if not found:
                # Add as new record
                self.unified_data[record['id']] = record
                self.stats['total_records'] += 1

    def validate_and_save(self):
        """Validate unified data, save to file, and insert to database"""
        logger.info("Validating unified data...")

        valid_records = []
        invalid_records = []

        for record_id, record in self.unified_data.items():
            is_valid, errors = self.validator.validate_record(record)

            if is_valid:
                valid_records.append(record)
            else:
                logger.warning(f"Validation errors for {record['name']}: {errors}")
                invalid_records.append(record)
                self.stats['validation_errors'] += 1

        # Connect to database and insert records
        if self.connect_to_database():
            logger.info(f"Inserting {len(valid_records)} valid records to database...")
            self.db_conn.autocommit = False  # Use transactions

            try:
                for i, record in enumerate(valid_records):
                    if i % 100 == 0 and i > 0:
                        logger.info(f"  Inserted {i}/{len(valid_records)} records to database...")
                        self.db_conn.commit()

                    self.insert_company_to_database(record)

                # Final commit
                self.db_conn.commit()
                logger.info(f"Database insertion complete! Inserted {self.stats['database_inserts']} records")

            except Exception as e:
                logger.error(f"Database transaction failed: {e}")
                self.db_conn.rollback()

            finally:
                self.close_database_connection()

        # Save valid records
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save main unified data file
        output_file = self.output_dir / f'unified_bds_data_{timestamp}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_records': len(valid_records),
                    'sources_processed': list(set(sum([r['data_sources'] for r in valid_records], []))),
                    'schema_version': '1.0',
                    'stats': self.stats
                },
                'companies': valid_records
            }, f, indent=2, ensure_ascii=False)

        # Save latest version
        latest_file = self.output_dir / 'unified_bds_data_latest.json'
        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'total_records': len(valid_records),
                    'sources_processed': list(set(sum([r['data_sources'] for r in valid_records], []))),
                    'schema_version': '1.0',
                    'stats': self.stats
                },
                'companies': valid_records
            }, f, indent=2, ensure_ascii=False)

        # Save CSV summary
        csv_file = self.output_dir / f'unified_bds_summary_{timestamp}.csv'
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['name', 'standard_name', 'parent_company', 'country_hq',
                         'industry', 'involvement_types', 'data_sources', 'confidence_score']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for record in valid_records:
                writer.writerow({
                    'name': record.get('name'),
                    'standard_name': record.get('standard_name'),
                    'parent_company': record.get('parent_company'),
                    'country_hq': record.get('country_hq'),
                    'industry': record.get('industry'),
                    'involvement_types': ', '.join(record.get('involvement_types', [])),
                    'data_sources': ', '.join(record.get('data_sources', [])),
                    'confidence_score': record.get('confidence_score', 0)
                })

        # Print summary
        logger.info("=" * 50)
        logger.info("Data Unification Complete!")
        logger.info(f"Total unique companies: {len(valid_records)}")
        logger.info(f"Duplicates merged: {self.stats['duplicates_merged']}")
        logger.info(f"Validation errors: {self.stats['validation_errors']}")
        logger.info(f"Database records inserted: {self.stats['database_inserts']}")
        logger.info(f"Database errors: {self.stats['database_errors']}")
        logger.info(f"Output saved to: {output_file}")
        logger.info(f"Summary saved to: {csv_file}")

        # Print top companies by confidence
        sorted_companies = sorted(valid_records,
                                 key=lambda x: x.get('confidence_score', 0),
                                 reverse=True)[:10]
        logger.info("\nTop 10 companies by confidence score:")
        for company in sorted_companies:
            logger.info(f"  - {company['name']}: {company.get('confidence_score', 0):.2f} "
                       f"(sources: {len(company.get('data_sources', []))})")


def main():
    """Main entry point"""
    output_dir = os.environ.get('OUTPUT_DIR', '/app/output')

    logger.info("Starting BDS Data Unification")
    logger.info(f"Output directory: {output_dir}")

    unifier = DataUnifier(output_dir)
    unifier.unify_all_sources()
    unifier.validate_and_save()


if __name__ == "__main__":
    main()