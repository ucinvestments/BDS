#!/usr/bin/env python3
"""
BDS Unified Schema Validator

This module provides validation functions for the unified BDS data schema.
It can validate individual records and batch validate multiple records.
"""

import json
import jsonschema
from jsonschema import validate, ValidationError, Draft7Validator
from typing import Dict, List, Any, Tuple
import os
from datetime import datetime

class BDSSchemaValidator:
    """Validator for BDS unified data schema"""

    def __init__(self, schema_path: str = "unified_schema.json"):
        """
        Initialize the validator with the schema

        Args:
            schema_path: Path to the JSON schema file
        """
        self.schema_path = schema_path
        self.schema = self._load_schema()
        self.validator = Draft7Validator(self.schema)

    def _load_schema(self) -> Dict:
        """Load the JSON schema from file"""
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")

        with open(self.schema_path, 'r') as f:
            return json.load(f)

    def validate_record(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate a single record against the schema

        Args:
            record: The data record to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        try:
            validate(instance=record, schema=self.schema)
            return True, []
        except ValidationError as e:
            # Collect all validation errors
            for error in self.validator.iter_errors(record):
                error_path = " -> ".join([str(p) for p in error.path])
                if error_path:
                    errors.append(f"{error_path}: {error.message}")
                else:
                    errors.append(error.message)
            return False, errors

    def validate_batch(self, records: List[Dict[str, Any]],
                      stop_on_error: bool = False) -> Dict[str, Any]:
        """
        Validate multiple records

        Args:
            records: List of records to validate
            stop_on_error: If True, stop validation on first error

        Returns:
            Dictionary with validation results
        """
        results = {
            "total": len(records),
            "valid": 0,
            "invalid": 0,
            "errors": {},
            "validation_time": datetime.now().isoformat()
        }

        for i, record in enumerate(records):
            record_id = record.get('id', f'record_{i}')
            is_valid, errors = self.validate_record(record)

            if is_valid:
                results["valid"] += 1
            else:
                results["invalid"] += 1
                results["errors"][record_id] = errors

                if stop_on_error:
                    break

        return results

    def generate_minimal_record(self) -> Dict[str, Any]:
        """
        Generate a minimal valid record with only required fields

        Returns:
            A minimal valid record
        """
        return {
            "id": "comp_example",
            "name": "Example Company",
            "reasons": [{
                "summary": "Example reason for listing"
            }],
            "data_sources": ["investigate.afsc.org"],
            "last_updated": datetime.now().isoformat()
        }

    def generate_complete_record(self) -> Dict[str, Any]:
        """
        Generate a complete example record with all fields

        Returns:
            A complete example record
        """
        return {
            "id": "comp_001_example",
            "name": "Example Corporation",
            "standard_name": "Example Corporation Inc",
            "aliases": ["Example Corp", "ExCorp"],
            "parent_company": "Parent Holdings LLC",
            "country_hq": "USA",
            "description": "A multinational corporation involved in various industries",

            "stock_symbols": [{
                "symbol": "EXMP",
                "exchange": "NASDAQ",
                "isin": "US0000000000"
            }],
            "industry": "Technology",
            "sectors": ["technology", "defense", "surveillance"],

            "involvement_types": ["military_support", "surveillance", "occupation"],
            "involvement_details": {
                "occupations": True,
                "prisons": False,
                "borders": True,
                "settlements": True,
                "military": True
            },
            "divestment_priority": "high",
            "booth_number": "42",

            "reasons": [{
                "summary": "Provides surveillance technology to military",
                "details": "The company has multiple contracts providing surveillance systems",
                "source": "https://example.com/evidence",
                "date_added": "2024-01-15"
            }],

            "sources": ["https://example.com/evidence"],
            "evidence_links": ["https://example.com/proof"],

            "boycott_actions": [
                "Don't use their products",
                "Cancel subscriptions",
                "Divest from stock"
            ],
            "alternatives": ["Alternative Company A", "Alternative Company B"],
            "campaigns": ["Campaign 2024", "Global Boycott Initiative"],

            "data_sources": ["investigate.afsc.org", "boycott.thewitness"],
            "last_updated": datetime.now().isoformat(),
            "confidence_score": 0.95,
            "verification_status": "verified"
        }


def main():
    """Example usage of the validator"""

    # Initialize validator
    validator = BDSSchemaValidator()

    print("BDS Schema Validator")
    print("=" * 50)

    # Test minimal record
    print("\n1. Testing minimal valid record:")
    minimal = validator.generate_minimal_record()
    is_valid, errors = validator.validate_record(minimal)
    print(f"   Valid: {is_valid}")
    if errors:
        print(f"   Errors: {errors}")

    # Test complete record
    print("\n2. Testing complete valid record:")
    complete = validator.generate_complete_record()
    is_valid, errors = validator.validate_record(complete)
    print(f"   Valid: {is_valid}")
    if errors:
        print(f"   Errors: {errors}")

    # Test invalid record
    print("\n3. Testing invalid record (missing required field):")
    invalid = {
        "name": "Invalid Company",
        "description": "Missing required fields"
    }
    is_valid, errors = validator.validate_record(invalid)
    print(f"   Valid: {is_valid}")
    if errors:
        for error in errors:
            print(f"   - {error}")

    # Test batch validation
    print("\n4. Testing batch validation:")
    batch = [minimal, complete, invalid]
    results = validator.validate_batch(batch)
    print(f"   Total: {results['total']}")
    print(f"   Valid: {results['valid']}")
    print(f"   Invalid: {results['invalid']}")
    if results['errors']:
        print("   Errors by record:")
        for record_id, record_errors in results['errors'].items():
            print(f"   - {record_id}:")
            for error in record_errors:
                print(f"     * {error}")


if __name__ == "__main__":
    main()