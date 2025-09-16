# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UC Investment Explorer - A web application that visualizes University of California investment data. The project consists of:
- Frontend: SvelteKit application for data visualization (hosted at http://ucinvestments.info/)
- Backend: Flask API server hosted on Heroku
- Data Processing: Python scripts for collecting, processing, and aggregating investment data
- BDS Service: Docker containerized web scraping service for company data

## Architecture

### Frontend (Webapp/)
- **Framework**: SvelteKit with TypeScript
- **Styling**: Tailwind CSS
- **Data Visualization**: D3.js
- **Analytics**: PostHog integration
- **Main Components**:
  - `/src/routes/+page.svelte`: Main investment visualization interface
  - `/src/routes/about/+page.svelte`: About page
  - `/src/routes/resources/+page.svelte`: Resources page
  - `/src/routes/ingest/+page.svelte`: Data ingestion interface
  - `/src/lib/`: Reusable components (loading, pie chart)
- **Deployment**: Vercel (configured via adapter-vercel)

### Backend (backend-server/)
- **Framework**: Flask with CORS support
- **Main Files**:
  - `main.py`: Flask API endpoints for serving investment data
  - `aggregator.py`: Investment data aggregation logic with fuzzy matching
- **API Endpoints**:
  - `/listed-assets`: Returns investment data from CSV
  - `/asset-classes`: Groups investments by asset class
  - `/company-composition/<class_grouping>/<estimation>`: Aggregated company data
  - `/company-composition/<class_grouping>/<estimation>/<query>`: Search functionality
- **API Base URL**: https://uc-investments-80f94956a47a.herokuapp.com
- **Deployment**: Heroku via gunicorn

### Data Processing (Data-Collection/)
- **Helper-Functions/**: Python scripts for data transformation
  - `combine-investments.py`: Combines investment data from multiple sources
  - `convert-CSVs-JSON.py`: Converts CSV files to JSON format
  - `fund-re-weighting.py`: Adjusts fund weights
  - `whale-wisdom-convertor.py`: Converts data from Whale Wisdom format
  - `pdf-investment-cleaner.py`: Extracts data from PDF reports
- **Data Directories**:
  - `csv-files/`: Raw CSV data for individual funds
  - `json-outputs/`: Processed JSON files
  - `final-fund-holdings/`: Processed fund holdings data
  - `individual-fund-outputs/`: Investment data by fund type

### BDS Service (BDS/)
- **Purpose**: Web scraping service for company data
- **Technology**: Python with BeautifulSoup4 and requests
- **Deployment**: Docker containerized service (who-profits-search)
- **Files**:
  - `main.py`: Web scraping implementation
  - `docker-compose.yml`: Container orchestration
  - `Dockerfile`: Python 3.11 base image

## Commands

### Frontend Development (in Webapp/ directory)
```bash
cd Webapp
npm install              # Install dependencies
npm run dev              # Start development server (localhost:5173)
npm run build            # Build for production
npm run preview          # Preview production build
npm run check            # Type checking with svelte-check
npm run format           # Auto-format code with Prettier
```

### Backend Development
```bash
pip install -r requirements.txt                    # Install Python dependencies
flask --app backend-server/main run               # Run Flask development server
gunicorn backend-server.main:app                  # Production server (as configured in Procfile)
```

### Data Processing
```bash
python Data-Collection/Helper-Functions/combine-investments.py     # Combine investment CSVs
python Data-Collection/Helper-Functions/convert-CSVs-JSON.py       # Convert CSVs to JSON
python backend-server/aggregator.py                                # Run data aggregation
```

### BDS Service
```bash
docker-compose up                                  # Start containerized web scraping service
docker build -t who-profits-search .              # Build Docker image
python BDS/main.py                                # Run scraper directly
```

## Key Data Flows

1. **Investment Data Collection**: Manual process (planned for automation)
   - UC releases investment reports
   - Data extracted and formatted into CSVs in `Data-Collection/csv-files/`
   - CSVs converted to JSON using helper scripts

2. **Data Aggregation**:
   - `aggregator.py` processes JSON files from `Data-Collection/json-outputs/`
   - Combines data with fund information from `final-datasets/listed_investments.csv`
   - Uses fuzzy matching (fuzzywuzzy library) for company name matching
   - Generates aggregated datasets in `final-datasets/` with different configurations

3. **Frontend Data Fetching**:
   - SvelteKit app fetches data from Flask API endpoints
   - Main endpoint: `/listed-assets` returns processed investment data
   - Data visualization using D3.js pie charts
   - Supports search and filtering by asset class

## Important Files

- `final-datasets/listed_investments.csv`: Master list of UC investments with funding sources
- `final-datasets/full_investments_*.json`: Aggregated investment data with different configurations (class grouping and estimation methods)
- `Data-Collection/csv-files/`: Fund composition data in CSV format (format for contributions)
- `Webapp/src/app.d.ts`: TypeScript type definitions for the application

## Development Notes

- Frontend uses TypeScript - ensure type safety when modifying components
- API responses are CORS-enabled for cross-origin requests from any domain
- Investment data format in CSVs should match existing files in `Data-Collection/csv-files/`
- The aggregator uses fuzzy string matching with a threshold of 90 for company name matching
- No formal test suite exists - consider manual testing when making changes
- The project is transitioning to automated data collection (currently manual)
- BDS service appears to scrape company information from external sources