package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
)

// CompanyInfo represents the result from Who Profits search
type CompanyInfo struct {
	CompanyName   string `json:"company_name"`
	TradedIn      string `json:"traded_in"`
	Headquarters  string `json:"headquarters"`
	Involvement   string `json:"involvement"`
	SearchTerm    string `json:"search_term"`
}

// Result represents the search result for a company
type Result struct {
	CompanyName string        `json:"company_name"`
	Found       bool          `json:"found"`
	Matches     []CompanyInfo `json:"matches"`
}

// Metadata contains search metadata
type Metadata struct {
	SearchDate         string `json:"search_date"`
	TotalCompanies     int    `json:"total_companies"`
	CompaniesFound     int    `json:"companies_found"`
	CompaniesNotFound  int    `json:"companies_not_found"`
}

// FinalOutput represents the complete output structure
type FinalOutput struct {
	Metadata Metadata          `json:"metadata"`
	Results  map[string]Result `json:"results"`
}

var companies = map[string]string{
	"20":  "Arm Guard",
	"21":  "Beghou",
	"22":  "BoonAl",
	"23":  "Nooks",
	"24":  "L'Oréal",
	"25":  "Clockwork Systems",
	"26":  "Sonatus",
	"27":  "JQ Investments",
	"28":  "C3.ai",
	"30":  "Qvest US",
	"31":  "Akuna Capital",
	"32":  "Credit One Bank",
	"33":  "Upstart",
	"34":  "Redwood Materials",
	"35":  "MCM",
	"36":  "CoinTracker",
	"37":  "Two Dots",
	"38":  "Canaan U.S. Inc",
	"40":  "Lawrence Livermore",
	"41":  "Kiso Technology",
	"42":  "Southern California Edison",
	"43":  "Hone Health",
	"44":  "Amgen",
	"45":  "CoStar Group",
	"46":  "Calpine Corporation",
	"47":  "Electronic Power Research Institute",
	"48":  "Glencore Ltd.",
	"50":  "Sandia National Laboratories",
	"51":  "Pacific Gas and Electric Company",
	"52":  "QuantumScape",
	"53":  "Johnson & Johnson",
	"54":  "Arete",
	"55":  "Blackhawk Network",
	"56":  "Rubrik",
	"57":  "Avangrid",
	"58":  "Aurora Energy Research",
	"60":  "ASM Guard",
	"61":  "Group One Trading LLC",
	"62":  "Affiliated Engineers, Inc.",
	"63":  "Boldt",
	"64":  "Bio-Rad Laboratories",
	"65":  "Inductive Automation",
	"66":  "Aperture LLC",
	"67":  "Southland Industries",
	"68":  "MEA Forensic Engineers & Scientists",
	"70":  "Peace Corps",
	"71":  "PAE Engineers",
	"72":  "Block",
	"73":  "GALLO",
	"74":  "Xenon Health",
	"75":  "Metronome",
	"76":  "EKI Environment & Water, Inc.",
	"77":  "Rambus",
	"78":  "Molex",
	"80":  "TSMC",
	"81":  "US Navy",
	"82":  "Epirus",
	"83":  "Army National Guard",
	"84":  "DiCon Fiberoptics, Inc.",
	"85":  "Kairos Power",
	"86":  "Martinez Refining Company",
	"87":  "Anning-Johnson Company",
	"88":  "Bloom Energy",
	"90":  "Aurora Energy Research",
	"91":  "KLA",
	"92":  "Huaqin Technology",
	"93":  "Epic",
	"94":  "Keck Graduate Institute",
	"95":  "Calico",
	"96":  "BioMarin",
	"97":  "ORISE FBI Visiting Scientist Program",
	"98":  "National Security Agency",
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
	"402": "Procter & Gamble",
}

func cleanCompanyName(name string) string {
	suffixes := []string{
		" LLC", " Inc.", " Inc", " Ltd.", " Ltd", " Corporation", " Corp.",
		" Corp", " Company", " Co.", " Group", " LLC", " (HPE)", " Guard",
	}
	
	cleanName := name
	for _, suffix := range suffixes {
		cleanName = strings.ReplaceAll(cleanName, suffix, "")
	}
	
	return strings.TrimSpace(cleanName)
}

func searchWhoProfits(companyName string) []CompanyInfo {
	baseURL := "https://www.whoprofits.org/companies/find"
	
	searchVariations := []string{
		companyName,
		cleanCompanyName(companyName),
	}
	
	// Add first word if multi-word company
	words := strings.Fields(companyName)
	if len(words) > 1 {
		searchVariations = append(searchVariations, words[0])
	}
	
	var allResults []CompanyInfo
	seenCompanies := make(map[string]bool)
	
	for _, searchTerm := range searchVariations {
		params := url.Values{
			"Text":       {searchTerm},
			"Name":       {""},
			"Category":   {""},
			"Sector":     {""},
			"Headquarter": {""},
			"Revenue":    {""},
			"Traded":     {""},
			"Presence":   {""},
			"Settlement": {""},
			"Type":       {"Table"},
		}
		
		fullURL := baseURL + "?" + params.Encode()
		
		client := &http.Client{
			Timeout: 10 * time.Second,
		}
		
		resp, err := client.Get(fullURL)
		if err != nil {
			log.Printf("Error searching for %s: %v", searchTerm, err)
			continue
		}
		defer resp.Body.Close()
		
		if resp.StatusCode != 200 {
			continue
		}
		
		doc, err := goquery.NewDocumentFromReader(resp.Body)
		if err != nil {
			log.Printf("Error parsing HTML for %s: %v", searchTerm, err)
			continue
		}
		
		// Find the search results table
		doc.Find("table.search-tbl tbody tr").Each(func(i int, s *goquery.Selection) {
			cols := s.Find("td")
			if cols.Length() >= 5 {
				companyInfo := CompanyInfo{
					CompanyName:  strings.TrimSpace(cols.Eq(1).Text()),
					TradedIn:     strings.TrimSpace(cols.Eq(2).Text()),
					Headquarters: strings.TrimSpace(cols.Eq(3).Text()),
					Involvement:  strings.TrimSpace(cols.Eq(4).Text()),
					SearchTerm:   searchTerm,
				}
				
				companyLower := strings.ToLower(companyInfo.CompanyName)
				searchLower := strings.ToLower(searchTerm)
				
				// Check if the result matches our search
				if strings.Contains(companyLower, searchLower) ||
					containsAnyWord(companyLower, searchLower) ||
					strings.Contains(companyLower, strings.ToLower(words[0])) {
					
					// Avoid duplicates
					if !seenCompanies[companyInfo.CompanyName] {
						allResults = append(allResults, companyInfo)
						seenCompanies[companyInfo.CompanyName] = true
					}
				}
			}
		})
		
		// Check if no results were found
		resultsNumber := doc.Find("h5.search-results-number").Text()
		if strings.TrimSpace(resultsNumber) == "0" {
			continue
		}
		
		time.Sleep(500 * time.Millisecond)
	}
	
	return allResults
}

func containsAnyWord(text, searchTerm string) bool {
	words := strings.Fields(searchTerm)
	for _, word := range words {
		if strings.Contains(text, strings.ToLower(word)) {
			return true
		}
	}
	return false
}

func main() {
	log.Println("Starting Who Profits search...")
	
	// Get output directory from environment variable
	outputDir := os.Getenv("OUTPUT_DIR")
	if outputDir == "" {
		outputDir = "/app/output"
	}
	
	// Ensure output directory exists
	err := os.MkdirAll(outputDir, 0755)
	if err != nil {
		log.Fatalf("Failed to create output directory: %v", err)
	}
	
	results := make(map[string]Result)
	metadata := Metadata{
		SearchDate:     time.Now().Format(time.RFC3339),
		TotalCompanies: len(companies),
	}
	
	log.Printf("Searching %d companies...", metadata.TotalCompanies)
	fmt.Println(strings.Repeat("-", 50))
	
	i := 1
	for booth, company := range companies {
		log.Printf("[%d/%d] Searching: %s (Booth %s)", i, metadata.TotalCompanies, company, booth)
		
		companyResults := searchWhoProfits(company)
		
		if len(companyResults) > 0 {
			results[booth] = Result{
				CompanyName: company,
				Found:       true,
				Matches:     companyResults,
			}
			metadata.CompaniesFound++
			log.Printf("  ✓ Found %d match(es)", len(companyResults))
		} else {
			results[booth] = Result{
				CompanyName: company,
				Found:       false,
				Matches:     []CompanyInfo{},
			}
			metadata.CompaniesNotFound++
			log.Printf("  ✗ No matches found")
		}
		
		time.Sleep(1 * time.Second)
		i++
	}
	
	// Create timestamped filename
	timestamp := time.Now().Format("20060102_150405")
	outputFile := fmt.Sprintf("%s/who_profits_results_%s.json", outputDir, timestamp)
	
	// Combine results and metadata
	finalOutput := FinalOutput{
		Metadata: metadata,
		Results:  results,
	}
	
	// Save results to JSON file
	jsonData, err := json.MarshalIndent(finalOutput, "", "  ")
	if err != nil {
		log.Fatalf("Failed to marshal JSON: %v", err)
	}
	
	err = os.WriteFile(outputFile, jsonData, 0644)
	if err != nil {
		log.Fatalf("Failed to write JSON file: %v", err)
	}
	
	// Also save a "latest" version
	latestFile := fmt.Sprintf("%s/who_profits_results_latest.json", outputDir)
	err = os.WriteFile(latestFile, jsonData, 0644)
	if err != nil {
		log.Printf("Failed to write latest file: %v", err)
	}
	
	fmt.Println(strings.Repeat("-", 50))
	log.Printf("Search complete! Results saved to %s", outputFile)
	
	// Print summary
	fmt.Println("\nSummary:")
	fmt.Printf("  Companies searched: %d\n", metadata.TotalCompanies)
	fmt.Printf("  Companies found in Who Profits: %d\n", metadata.CompaniesFound)
	fmt.Printf("  Companies not found: %d\n", metadata.CompaniesNotFound)
	
	// Print list of companies found
	if metadata.CompaniesFound > 0 {
		fmt.Println("\nCompanies found in Who Profits database:")
		for booth, data := range results {
			if data.Found {
				fmt.Printf("  - Booth %s: %s\n", booth, data.CompanyName)
				for _, match := range data.Matches {
					fmt.Printf("    → %s (%s)\n", match.CompanyName, match.Headquarters)
				}
			}
		}
	}
	
	// Create a summary CSV file
	summaryFile := fmt.Sprintf("%s/who_profits_summary_%s.csv", outputDir, timestamp)
	csvFile, err := os.Create(summaryFile)
	if err != nil {
		log.Printf("Failed to create CSV file: %v", err)
	} else {
		defer csvFile.Close()
		
		writer := csv.NewWriter(csvFile)
		defer writer.Flush()
		
		// Write header
		writer.Write([]string{"Booth", "Company Name", "Found in Who Profits", "Matches"})
		
		// Write data
		for booth, data := range results {
			var matches string
			if len(data.Matches) > 0 {
				var matchNames []string
				for _, m := range data.Matches {
					matchNames = append(matchNames, m.CompanyName)
				}
				matches = strings.Join(matchNames, "; ")
			} else {
				matches = "None"
			}
			
			writer.Write([]string{
				booth,
				data.CompanyName,
				fmt.Sprintf("%v", data.Found),
				matches,
			})
		}
		
		log.Printf("Summary CSV saved to %s", summaryFile)
	}
}