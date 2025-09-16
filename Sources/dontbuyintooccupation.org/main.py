import requests
from bs4 import BeautifulSoup
import json
import time
import os
import logging
from datetime import datetime
from urllib.parse import quote

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get output directory from environment variable
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/app/output')

# Company data with booth numbers
companies = {
    "20": "Arm Guard",
    "21": "Beghou",
    "22": "BoonAl",
    "23": "Nooks",
    "24": "L'Oréal",
    "25": "Clockwork Systems",
    "26": "Sonatus",
    "27": "JQ Investments",
    "28": "C3.ai",
    "30": "Qvest US",
    "31": "Akuna Capital",
    "32": "Credit One Bank",
    "33": "Upstart",
    "34": "Redwood Materials",
    "35": "MCM",
    "36": "CoinTracker",
    "37": "Two Dots",
    "38": "Canaan U.S. Inc",
    "40": "Lawrence Livermore",
    "41": "Kiso Technology",
    "42": "Southern California Edison",
    "43": "Hone Health",
    "44": "Amgen",
    "45": "CoStar Group",
    "46": "Calpine Corporation",
    "47": "Electronic Power Research Institute",
    "48": "Glencore Ltd.",
    "50": "Sandia National Laboratories",
    "51": "Pacific Gas and Electric Company",
    "52": "QuantumScape",
    "53": "Johnson & Johnson",
    "54": "Arete",
    "55": "Blackhawk Network",
    "56": "Rubrik",
    "57": "Avangrid",
    "58": "Aurora Energy Research",
    "60": "ASM Guard",
    "61": "Group One Trading LLC",
    "62": "Affiliated Engineers, Inc.",
    "63": "Boldt",
    "64": "Bio-Rad Laboratories",
    "65": "Inductive Automation",
    "66": "Aperture LLC",
    "67": "Southland Industries",
    "68": "MEA Forensic Engineers & Scientists",
    "70": "Peace Corps",
    "71": "PAE Engineers",
    "72": "Block",
    "73": "GALLO",
    "74": "Xenon Health",
    "75": "Metronome",
    "76": "EKI Environment & Water, Inc.",
    "77": "Rambus",
    "78": "Molex",
    "80": "TSMC",
    "81": "US Navy",
    "82": "Epirus",
    "83": "Army National Guard",
    "84": "DiCon Fiberoptics, Inc.",
    "85": "Kairos Power",
    "86": "Martinez Refining Company",
    "87": "Anning-Johnson Company",
    "88": "Bloom Energy",
    "90": "Aurora Energy Research",
    "91": "KLA",
    "92": "Huaqin Technology",
    "93": "Epic",
    "94": "Keck Graduate Institute",
    "95": "Calico",
    "96": "BioMarin",
    "97": "ORISE FBI Visiting Scientist Program",
    "98": "National Security Agency",
    "100": "Workday, Inc",
    "101": "Eli Lilly and Company",
    "102": "Hewlett Packard Enterprise (HPE)",
    "103": "Fieldguide",
    "104": "Matroid, Inc",
    "105": "Sourcegraph",
    "106": "AVEVA",
    "107": "SICK",
    "108": "Seven Research",
    "109": "Aven",
    "200": "KOTRA Silicon Valley",
    "201": "ACCO Engineered Systems",
    "202": "Micron Technology",
    "203": "Pantex",
    "204": "Elve, Inc",
    "205": "Lifespan Research Institute",
    "206": "LightSource",
    "207": "Trinity Life Sciences",
    "208": "Science Corporation",
    "209": "California State Water Resources Control Board",
    "210": "Central Intelligence Agency",
    "300": "Altruist",
    "301": "Lightmatter",
    "400": "Cisco Systems Guard",
    "401": "Applied Materials",
    "402": "Procter & Gamble"
}

def clean_company_name(name):
    """Clean company name for better search matching"""
    suffixes = [
        " LLC", " Inc.", " Inc", " Ltd.", " Ltd", " Corporation", " Corp.",
        " Corp", " Company", " Co.", " Group", " LLC", " (HPE)", " Guard"
    ]
    
    clean_name = name
    for suffix in suffixes:
        clean_name = clean_name.replace(suffix, "")
    
    return clean_name.strip()

def search_who_profits(company_name):
    """Search Who Profits database for a company"""
    base_url = "https://www.whoprofits.org/companies/find"
    
    search_variations = [
        company_name,
        clean_company_name(company_name),
        company_name.split()[0] if len(company_name.split()) > 1 else company_name
    ]
    
    all_results = []
    
    for search_term in search_variations:
        params = {
            'Text': search_term,
            'Name': '',
            'Category': '',
            'Sector': '',
            'Headquarter': '',
            'Revenue': '',
            'Traded': '',
            'Presence': '',
            'Settlement': '',
            'Type': 'Table'
        }
        
        try:
            logger.debug(f"Searching with term: {search_term}")
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                table = soup.find('table', class_='search-tbl')
                
                if table:
                    tbody = table.find('tbody')
                    if tbody:
                        rows = tbody.find_all('tr')
                        
                        for row in rows:
                            cols = row.find_all('td')
                            if len(cols) >= 5:
                                company_info = {
                                    'company_name': cols[1].get_text(strip=True),
                                    'traded_in': cols[2].get_text(strip=True),
                                    'headquarters': cols[3].get_text(strip=True),
                                    'involvement': cols[4].get_text(strip=True),
                                    'search_term': search_term
                                }
                                
                                company_lower = company_info['company_name'].lower()
                                search_lower = search_term.lower()
                                
                                if (search_lower in company_lower or 
                                    any(word in company_lower for word in search_lower.split()) or
                                    search_lower.split()[0] in company_lower):
                                    
                                    if not any(r['company_name'] == company_info['company_name'] for r in all_results):
                                        all_results.append(company_info)
                
                if not all_results:
                    results_number = soup.find('h5', class_='search-results-number')
                    if results_number and results_number.get_text(strip=True) == '0':
                        continue
                        
        except requests.RequestException as e:
            logger.error(f"Error searching for {search_term}: {e}")
        
        time.sleep(0.5)
    
    return all_results

def main():
    """Main function to search all companies and save results"""
    logger.info("Starting Who Profits search...")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    results = {}
    metadata = {
        'search_date': datetime.now().isoformat(),
        'total_companies': len(companies),
        'companies_found': 0,
        'companies_not_found': 0
    }
    
    total_companies = len(companies)
    
    logger.info(f"Searching {total_companies} companies...")
    print("-" * 50)
    
    for i, (booth, company) in enumerate(companies.items(), 1):
        logger.info(f"[{i}/{total_companies}] Searching: {company} (Booth {booth})")
        
        company_results = search_who_profits(company)
        
        if company_results:
            results[booth] = {
                'company_name': company,
                'found': True,
                'matches': company_results
            }
            metadata['companies_found'] += 1
            logger.info(f"  ✓ Found {len(company_results)} match(es)")
        else:
            results[booth] = {
                'company_name': company,
                'found': False,
                'matches': []
            }
            metadata['companies_not_found'] += 1
            logger.info(f"  ✗ No matches found")
        
        time.sleep(1)
    
    # Create timestamped filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(OUTPUT_DIR, f'who_profits_results_{timestamp}.json')
    
    # Combine results and metadata
    final_output = {
        'metadata': metadata,
        'results': results
    }
    
    # Save results to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    # Also save a "latest" version
    latest_file = os.path.join(OUTPUT_DIR, 'who_profits_results_latest.json')
    with open(latest_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)
    
    print("-" * 50)
    logger.info(f"Search complete! Results saved to {output_file}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Companies searched: {metadata['total_companies']}")
    print(f"  Companies found in Who Profits: {metadata['companies_found']}")
    print(f"  Companies not found: {metadata['companies_not_found']}")
    
    # Print list of companies found
    if metadata['companies_found'] > 0:
        print("\nCompanies found in Who Profits database:")
        for booth, data in results.items():
            if data['found']:
                print(f"  - Booth {booth}: {data['company_name']}")
                for match in data['matches']:
                    print(f"    → {match['company_name']} ({match['headquarters']})")
    
    # Create a summary CSV file for easy reading
    summary_file = os.path.join(OUTPUT_DIR, f'who_profits_summary_{timestamp}.csv')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Booth,Company Name,Found in Who Profits,Matches\n")
        for booth, data in results.items():
            matches = "; ".join([m['company_name'] for m in data['matches']]) if data['matches'] else "None"
            f.write(f"{booth},{data['company_name']},{data['found']},{matches}\n")
    
    logger.info(f"Summary CSV saved to {summary_file}")

if __name__ == "__main__":
    main()
