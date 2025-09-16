# Unified BDS Data Schema

## Overview
This document defines a unified data schema for consolidating information from multiple BDS (Boycott, Divestment, Sanctions) data sources into a single, consistent format.

## Core Entity: Company/Organization

### Primary Fields

| Field | Type | Required | Description | Source Mappings |
|-------|------|----------|-------------|-----------------|
| `id` | string | Yes | Unique identifier (generated) | Auto-generated |
| `name` | string | Yes | Primary company/organization name | All sources |
| `standard_name` | string | No | Standardized legal name | AFSC: Company Standard Name |
| `aliases` | array[string] | No | Alternative names, subsidiaries | Derived from multiple sources |
| `parent_company` | string | No | Parent company if subsidiary | BDS Coalition: Parent Company |
| `country_hq` | string | No | Country of headquarters | AFSC: Country of HQ, BDS Coalition: Country |
| `description` | string | No | Brief company description | All sources |

### Financial Information

| Field | Type | Required | Description | Source Mappings |
|-------|------|----------|-------------|-----------------|
| `stock_symbols` | array[object] | No | Stock ticker information | AFSC data |
| ├─ `symbol` | string | Yes | Ticker symbol | AFSC: Primary Symbol |
| ├─ `exchange` | string | Yes | Exchange name | AFSC: Primary Exchange Name |
| └─ `isin` | string | No | International Securities ID | AFSC: Primary ISIN |
| `industry` | string | No | Primary industry classification | AFSC: Industry |
| `sectors` | array[string] | No | Business sectors | Boycott.thewitness: categories |

### BDS-Related Information

| Field | Type | Required | Description | Source Mappings |
|-------|------|----------|-------------|-----------------|
| `involvement_types` | array[string] | No | Types of problematic involvement | See "Involvement Types" section |
| `involvement_details` | object | No | Detailed involvement information | |
| ├─ `occupations` | boolean | No | Involved in occupations | AFSC: Occupations |
| ├─ `prisons` | boolean | No | Prison industry involvement | AFSC: Prisons |
| ├─ `borders` | boolean | No | Border militarization | AFSC: Borders |
| ├─ `settlements` | boolean | No | Israeli settlement activity | Derived from descriptions |
| └─ `military` | boolean | No | Military/weapons involvement | Derived from descriptions |
| `divestment_priority` | string | No | Priority level for divestment | AFSC: Divestment Shortlist |
| `booth_number` | string | No | Event booth number if applicable | Who Profits search: booth |

### Evidence and Documentation

| Field | Type | Required | Description | Source Mappings |
|-------|------|----------|-------------|-----------------|
| `reasons` | array[object] | Yes | Reasons for listing | |
| ├─ `summary` | string | Yes | Brief reason | All sources |
| ├─ `details` | string | No | Detailed explanation | Various description fields |
| ├─ `source` | string | No | Source URL/reference | BDS Coalition: Sources/Links |
| └─ `date_added` | date | No | When reason was documented | |
| `sources` | array[string] | No | All source URLs/references | All source link fields |
| `evidence_links` | array[string] | No | Direct evidence URLs | Various source fields |

### Action Information

| Field | Type | Required | Description | Source Mappings |
|-------|------|----------|-------------|-----------------|
| `boycott_actions` | array[string] | No | Specific boycott actions | Boycott.thewitness: how_to_boycott |
| `alternatives` | array[string] | No | Alternative companies/products | Boycott.thewitness: alternatives |
| `campaigns` | array[string] | No | Active campaign names | Derived from sources |

### Metadata

| Field | Type | Required | Description | Source Mappings |
|-------|------|----------|-------------|-----------------|
| `data_sources` | array[string] | Yes | Which sources provided data | Track during import |
| `last_updated` | datetime | Yes | Last data update | Import timestamp |
| `confidence_score` | float | No | Data confidence (0-1) | Based on source matches |
| `verification_status` | string | No | verified/unverified/disputed | Manual review field |

## Involvement Types Enum

Standard values for `involvement_types`:
- `occupation` - Supporting occupation of Palestinian territories
- `settlements` - Operating in or supporting illegal settlements
- `military_support` - Providing military equipment/services
- `prison_industry` - Prison labor or services
- `border_security` - Border militarization technology
- `surveillance` - Surveillance technology used for oppression
- `financial_support` - Direct financial support to problematic entities
- `normalization` - Normalization activities
- `labor_violations` - Labor rights violations
- `environmental` - Environmental violations in occupied territories

## Example Record

```json
{
  "id": "comp_001_amazon",
  "name": "Amazon",
  "standard_name": "Amazon.com Inc",
  "aliases": ["Amazon Web Services", "AWS"],
  "parent_company": null,
  "country_hq": "USA",
  "description": "The world's largest online retailer and cloud storage provider",

  "stock_symbols": [{
    "symbol": "AMZN",
    "exchange": "NASDAQ",
    "isin": "US0231351067"
  }],
  "industry": "Specialty Retail",
  "sectors": ["technology", "retail", "cloud"],

  "involvement_types": ["occupation", "military_support", "surveillance", "prison_industry"],
  "involvement_details": {
    "occupations": true,
    "prisons": true,
    "borders": true,
    "settlements": false,
    "military": true
  },
  "divestment_priority": null,

  "reasons": [{
    "summary": "Provides cloud computing to Israeli military",
    "details": "Amazon Web Services hosts Israeli military and governmental systems. The company has contracts with the Israeli military and provides cloud computing services that enable surveillance and military operations against Palestinians.",
    "source": "https://investigate.info/company/amazon",
    "date_added": "2024-01-15"
  }],

  "sources": [
    "https://investigate.info/company/amazon",
    "https://example.com/proof-link"
  ],

  "boycott_actions": [
    "Don't shop on Amazon.com",
    "Cancel Amazon Prime",
    "Don't use Amazon Web Services"
  ],
  "alternatives": ["Local stores", "eBay", "Direct from manufacturer websites"],

  "data_sources": ["investigate.afsc.org", "boycott.thewitness"],
  "last_updated": "2025-09-15T10:30:00Z",
  "confidence_score": 0.95,
  "verification_status": "verified"
}
```

## Data Merging Strategy

When combining data from multiple sources:

1. **Name Matching**: Use fuzzy matching (threshold: 85%) to identify same entities across sources
2. **Priority Order**: When conflicts arise, prioritize sources in this order:
   - AFSC Investigate (most comprehensive financial data)
   - BDS Coalition (broadest coverage)
   - Boycott.thewitness (detailed boycott actions)
   - Who Profits search (specific event data)
3. **Aggregation Rules**:
   - Combine all unique reasons and sources
   - Union all involvement types
   - Keep most recent description
   - Merge all alternative names into aliases
   - Combine all boycott actions and alternatives

## Implementation Notes

- Use company name normalization (remove Inc., Ltd., etc.) for matching
- Generate stable IDs based on normalized company names
- Track data lineage by maintaining source information
- Implement validation to ensure required fields are present
- Consider implementing a confidence scoring system based on number of confirming sources