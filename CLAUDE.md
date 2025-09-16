# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BDS (Boycott, Divestment, Sanctions) data collection and analysis repository containing multiple web scraping services that gather information about companies and their relationships. The project includes a unified data schema for consolidating information from diverse sources.

## Architecture

The project consists of independent data collection services in the `Sources/` directory:

### dontbuyintooccupation.org Service
- **Purpose**: Searches the Who Profits database for company information
- **Technology**: Python with BeautifulSoup4 for web scraping
- **Main Script**: `main.py` - Searches a predefined list of companies (with booth numbers) and outputs results
- **Deployment**: Docker containerized service (`who-profits-search`)
- **Output**: JSON results with company matches and CSV summaries

### boycott.thewitness Service
- **Purpose**: Web scraping service for boycott-related data
- **Technology**: Go-based scraper
- **Files**: `boycott_scraper.go` and `boycott_scraper_enhanced.go`
- **Deployment**: Docker containerized service (`boycott-thewitness-scraper`)

### Data Sources
- **bdscoalition.ca/**: Contains BDS Shame List CSV data
- **investigate.afsc.org/**: Contains investigate dataset in CSV/XLSX format

### Unified Data Schema
- **Location**: `Sources/Unified/` directory
- **Schema Definition**: `unified_schema.json` - JSON Schema for validation
- **Documentation**: `unified_schema.md` - Human-readable field mappings and examples
- **Validator**: `schema_validator.py` - Python validation tool with batch processing

## Commands

### Running the Who Profits Scraper
```bash
cd Sources/dontbuyintooccupation.org

# Install Python dependencies
pip install -r requirements.txt

# Run directly
python main.py

# Run with Docker
docker-compose up

# Build Docker image
docker build -t who-profits-search .
```

### Running the Boycott Scraper
```bash
cd Sources/boycott.thewitness

# Run with Docker
docker-compose up

# Build Docker image
docker build -t boycott-thewitness-scraper .
```

### Validating Data Against Unified Schema
```bash
cd Sources/Unified

# Install dependencies (jsonschema)
pip install jsonschema

# Run validator with example data
python schema_validator.py

# Validate custom data file
python -c "from schema_validator import BDSSchemaValidator; v = BDSSchemaValidator(); print(v.validate_record(your_data))"
```

## Key Implementation Details

### Who Profits Scraper (dontbuyintooccupation.org/main.py)
- Searches companies against https://www.whoprofits.org/companies/find
- Uses multiple search variations (full name, cleaned name, first word)
- Implements fuzzy matching to identify relevant results
- Outputs include:
  - Timestamped JSON results with metadata
  - Latest results file for easy access
  - CSV summary for quick analysis
- Rate limiting: 0.5-1 second delay between searches

### Data Output Structure
All scrapers output to their respective `output/` directories with:
- Timestamped result files for historical tracking
- "Latest" versions for easy access
- JSON format for structured data
- CSV summaries for spreadsheet analysis

### Unified Schema Structure
The unified schema (`Sources/Unified/unified_schema.json`) consolidates data from all sources with:
- Core company identification fields (name, aliases, parent company)
- Financial information (stock symbols, industry sectors)
- BDS involvement categorization (occupation, settlements, military support, etc.)
- Evidence documentation (reasons, sources, links)
- Action information (boycott actions, alternatives)
- Data lineage tracking (source attribution, confidence scoring)

## Environment Variables

- `OUTPUT_DIR`: Directory for saving scraper results (default: `/app/output`)
- `LOG_LEVEL`: Logging verbosity (default: `INFO`)
- `PYTHONUNBUFFERED`: Set to 1 for real-time output in Docker