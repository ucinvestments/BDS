package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
)

// Brand represents a boycott target brand with detailed information
type Brand struct {
	Name          string    `json:"name"`
	ImageURL      string    `json:"image_url"`
	TargetLink    string    `json:"target_link"`
	PageNumber    int       `json:"page_number"`
	ScrapedAt     time.Time `json:"scraped_at"`
	
	// Detailed information from individual pages
	ID            string    `json:"id,omitempty"`
	Description   string    `json:"description,omitempty"`
	Reason        string    `json:"reason,omitempty"`
	Categories    []string  `json:"categories,omitempty"`
	HowToBoycott  []string  `json:"how_to_boycott,omitempty"`
	Alternatives  []string  `json:"alternatives,omitempty"`
	Source        string    `json:"source,omitempty"`
	DetailsFetched bool     `json:"details_fetched"`
	DetailsError   string    `json:"details_error,omitempty"`
}

// ScrapeResult holds all scraped data
type ScrapeResult struct {
	TotalBrands       int       `json:"total_brands"`
	TotalPages        int       `json:"total_pages"`
	BrandsWithDetails int       `json:"brands_with_details"`
	Brands            []Brand   `json:"brands"`
	ScrapedAt         time.Time `json:"scraped_at"`
	LastPageEmpty     bool      `json:"last_page_empty"`
}

// TargetPageData represents the JSON data embedded in target pages
type TargetPageData struct {
	Props struct {
		PageProps struct {
			Listing struct {
				ID           string   `json:"id"`
				Name         string   `json:"name"`
				Logo         string   `json:"logo"`
				Description  string   `json:"description"`
				Reason       string   `json:"reason"`
				Category     []string `json:"category"`
				HowToBoycott []string `json:"howToBoycott"`
				Alternatives []string `json:"alternatives"`
				Source       string   `json:"source"`
			} `json:"listing"`
		} `json:"pageProps"`
	} `json:"props"`
}

func main() {
	log.Println("Starting Enhanced Boycott The Witness scraper...")

	// Get output directory from environment or use default
	outputDir := os.Getenv("OUTPUT_DIR")
	if outputDir == "" {
		outputDir = "/output"
	}

	// Check if we should fetch details (can be disabled for faster scraping)
	fetchDetails := os.Getenv("FETCH_DETAILS") != "false"
	
	// Batch size for detail fetching to avoid overwhelming the server
	batchSize := 10
	if batchSizeEnv := os.Getenv("BATCH_SIZE"); batchSizeEnv != "" {
		fmt.Sscanf(batchSizeEnv, "%d", &batchSize)
	}

	log.Printf("Fetch details: %v, Batch size: %d", fetchDetails, batchSize)

	// Ensure output directory exists
	err := os.MkdirAll(outputDir, 0755)
	if err != nil {
		log.Fatalf("Failed to create output directory: %v", err)
	}

	result := ScrapeResult{
		Brands:    []Brand{},
		ScrapedAt: time.Now(),
	}

	// Step 1: Scrape all brands from browse pages
	log.Println("Step 1: Scraping brand list from browse pages...")
	brands, totalPages := scrapeBrandList()
	result.Brands = brands
	result.TotalPages = totalPages
	result.TotalBrands = len(brands)

	// Step 2: Fetch detailed information if enabled
	if fetchDetails && len(brands) > 0 {
		log.Printf("Step 2: Fetching detailed information for %d brands...", len(brands))
		result.Brands = fetchBrandDetails(brands, batchSize)
		
		// Count brands with successful detail fetch
		for _, brand := range result.Brands {
			if brand.DetailsFetched {
				result.BrandsWithDetails++
			}
		}
	}

	// Save results
	saveResults(result, outputDir)

	// Print summary
	printSummary(result)
}

func scrapeBrandList() ([]Brand, int) {
	var brands []Brand
	baseURL := "https://boycott.thewitness.news/browse/"
	pageNumber := 1
	emptyPageCount := 0
	maxEmptyPages := 3

	for {
		log.Printf("Scraping brand list from page %d...", pageNumber)
		
		pageBrands, err := scrapePage(fmt.Sprintf("%s%d", baseURL, pageNumber))
		if err != nil {
			log.Printf("Error scraping page %d: %v", pageNumber, err)
			emptyPageCount++
			
			if emptyPageCount >= maxEmptyPages {
				log.Printf("Reached %d consecutive empty pages, stopping...", maxEmptyPages)
				break
			}
			
			pageNumber++
			time.Sleep(1 * time.Second)
			continue
		}

		if len(pageBrands) == 0 {
			emptyPageCount++
			log.Printf("Page %d returned no brands (empty page count: %d)", pageNumber, emptyPageCount)
			
			if emptyPageCount >= maxEmptyPages {
				log.Printf("Reached %d consecutive empty pages, stopping...", maxEmptyPages)
				break
			}
		} else {
			emptyPageCount = 0
			log.Printf("Found %d brands on page %d", len(pageBrands), pageNumber)
			
			// Add page number to each brand
			for i := range pageBrands {
				pageBrands[i].PageNumber = pageNumber
			}
			
			brands = append(brands, pageBrands...)
		}

		pageNumber++
		time.Sleep(1 * time.Second)
		
		// Safety limit
		if pageNumber > 100 {
			log.Println("Reached maximum page limit (100), stopping...")
			break
		}
	}

	return brands, pageNumber - 1
}

func scrapePage(url string) ([]Brand, error) {
	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch page: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("received status code %d", resp.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse HTML: %w", err)
	}

	var brands []Brand

	// Look for brand cards
	doc.Find("div.m-e615b15f.mantine-Card-root").Each(func(i int, s *goquery.Selection) {
		// Skip featured news cards
		if s.Find("p").Text() == "Featured news" {
			return
		}

		brand := Brand{
			ScrapedAt: time.Now(),
		}

		// Extract brand name
		nameElem := s.Find("p.mantine-Text-root[data-size='lg']")
		if nameElem.Length() > 0 {
			brand.Name = strings.TrimSpace(nameElem.Text())
		}

		// Extract image URL
		imgElem := s.Find("img.m-11f8ac07.mantine-Avatar-image")
		if imgElem.Length() > 0 {
			brand.ImageURL, _ = imgElem.Attr("src")
		}

		// Extract target link
		linkElem := s.Find("a[href^='/target/']")
		if linkElem.Length() > 0 {
			href, exists := linkElem.Attr("href")
			if exists {
				brand.TargetLink = href
				// Extract ID from target link
				if parts := strings.Split(href, "/"); len(parts) > 2 {
					brand.ID = parts[2]
				}
			}
		}

		// Only add if we found a name
		if brand.Name != "" && brand.Name != "Featured news" {
			brands = append(brands, brand)
		}
	})

	// Fallback selector if needed
	if len(brands) == 0 {
		doc.Find("a[href^='/target/']").Each(func(i int, s *goquery.Selection) {
			href, _ := s.Attr("href")
			
			card := s.ParentsFiltered("div.mantine-Card-root").First()
			if card.Length() > 0 {
				brand := Brand{
					ScrapedAt:  time.Now(),
					TargetLink: href,
				}
				
				if parts := strings.Split(href, "/"); len(parts) > 2 {
					brand.ID = parts[2]
				}
				
				nameElem := card.Find("p[data-size='lg']")
				if nameElem.Length() > 0 {
					brand.Name = strings.TrimSpace(nameElem.Text())
				}
				
				imgElem := card.Find("img").First()
				if imgElem.Length() > 0 {
					brand.ImageURL, _ = imgElem.Attr("src")
				}
				
				if brand.Name != "" {
					isDuplicate := false
					for _, existing := range brands {
						if existing.Name == brand.Name {
							isDuplicate = true
							break
						}
					}
					if !isDuplicate {
						brands = append(brands, brand)
					}
				}
			}
		})
	}

	return brands, nil
}

func fetchBrandDetails(brands []Brand, batchSize int) []Brand {
	updatedBrands := make([]Brand, len(brands))
	copy(updatedBrands, brands)

	for i := 0; i < len(updatedBrands); i += batchSize {
		end := i + batchSize
		if end > len(updatedBrands) {
			end = len(updatedBrands)
		}

		log.Printf("Fetching details for brands %d-%d of %d", i+1, end, len(updatedBrands))

		// Process batch
		for j := i; j < end; j++ {
			brand := &updatedBrands[j]
			
			if brand.TargetLink == "" {
				brand.DetailsError = "No target link available"
				continue
			}

			details, err := fetchBrandDetail("https://boycott.thewitness.news" + brand.TargetLink)
			if err != nil {
				log.Printf("Error fetching details for %s: %v", brand.Name, err)
				brand.DetailsError = err.Error()
				continue
			}

			// Update brand with detailed information
			brand.Description = details.Props.PageProps.Listing.Description
			brand.Reason = details.Props.PageProps.Listing.Reason
			brand.Categories = details.Props.PageProps.Listing.Category
			brand.HowToBoycott = details.Props.PageProps.Listing.HowToBoycott
			brand.Alternatives = details.Props.PageProps.Listing.Alternatives
			brand.Source = details.Props.PageProps.Listing.Source
			brand.DetailsFetched = true

			log.Printf("✓ Fetched details for: %s", brand.Name)
		}

		// Rate limiting between batches
		if end < len(updatedBrands) {
			log.Printf("Batch complete, waiting 2 seconds before next batch...")
			time.Sleep(2 * time.Second)
		}
	}

	return updatedBrands
}

func fetchBrandDetail(url string) (*TargetPageData, error) {
	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch page: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("received status code %d", resp.StatusCode)
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse HTML: %w", err)
	}

	// Find the JSON data in the script tag
	var jsonData string
	doc.Find("script#__NEXT_DATA__").Each(func(i int, s *goquery.Selection) {
		jsonData = s.Text()
	})

	if jsonData == "" {
		return nil, fmt.Errorf("no JSON data found in page")
	}

	// Parse JSON data
	var pageData TargetPageData
	err = json.Unmarshal([]byte(jsonData), &pageData)
	if err != nil {
		return nil, fmt.Errorf("failed to parse JSON data: %w", err)
	}

	// Rate limiting
	time.Sleep(500 * time.Millisecond)

	return &pageData, nil
}

func saveResults(result ScrapeResult, outputDir string) {
	timestamp := time.Now().Format("20060102_150405")
	
	// Save JSON
	outputFile := filepath.Join(outputDir, fmt.Sprintf("boycott_brands_enhanced_%s.json", timestamp))
	jsonData, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		log.Printf("Failed to marshal JSON: %v", err)
		return
	}

	err = os.WriteFile(outputFile, jsonData, 0644)
	if err != nil {
		log.Printf("Failed to write JSON file: %v", err)
		return
	}

	// Save latest version
	latestFile := filepath.Join(outputDir, "boycott_brands_enhanced_latest.json")
	err = os.WriteFile(latestFile, jsonData, 0644)
	if err != nil {
		log.Printf("Failed to write latest file: %v", err)
	}

	// Save CSV
	csvFile := filepath.Join(outputDir, fmt.Sprintf("boycott_brands_enhanced_%s.csv", timestamp))
	err = writeEnhancedCSV(csvFile, result.Brands)
	if err != nil {
		log.Printf("Failed to write CSV file: %v", err)
	}

	log.Printf("Results saved to: %s", outputFile)
}

func writeEnhancedCSV(filename string, brands []Brand) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	// Write header
	fmt.Fprintln(file, "Name,Target Link,Image URL,Page Number,Description,Reason,Categories,How To Boycott,Alternatives,Source,Details Fetched,Details Error,Scraped At")

	// Write data
	for _, brand := range brands {
		// Clean and escape fields
		name := strings.ReplaceAll(brand.Name, ",", ";")
		description := strings.ReplaceAll(brand.Description, ",", ";")
		reason := strings.ReplaceAll(brand.Reason, ",", ";")
		categories := strings.Join(brand.Categories, " | ")
		howToBoycott := strings.Join(brand.HowToBoycott, " | ")
		alternatives := strings.Join(brand.Alternatives, " | ")
		source := strings.ReplaceAll(brand.Source, ",", ";")
		detailsError := strings.ReplaceAll(brand.DetailsError, ",", ";")
		
		fmt.Fprintf(file, "%s,%s,%s,%d,%s,%s,%s,%s,%s,%s,%v,%s,%s\n",
			name,
			brand.TargetLink,
			brand.ImageURL,
			brand.PageNumber,
			description,
			reason,
			categories,
			howToBoycott,
			alternatives,
			source,
			brand.DetailsFetched,
			detailsError,
			brand.ScrapedAt.Format(time.RFC3339),
		)
	}

	return nil
}

func printSummary(result ScrapeResult) {
	fmt.Println("\n" + strings.Repeat("=", 60))
	fmt.Printf("Enhanced Scraping Complete!\n")
	fmt.Printf("Total pages scraped: %d\n", result.TotalPages)
	fmt.Printf("Total brands found: %d\n", result.TotalBrands)
	fmt.Printf("Brands with detailed info: %d\n", result.BrandsWithDetails)
	
	if result.TotalBrands > 0 {
		successRate := float64(result.BrandsWithDetails) / float64(result.TotalBrands) * 100
		fmt.Printf("Detail fetch success rate: %.1f%%\n", successRate)
	}
	
	if result.TotalBrands > 0 {
		fmt.Println("\nSample of brands with details:")
		limit := 5
		if len(result.Brands) < limit {
			limit = len(result.Brands)
		}
		
		for i := 0; i < limit; i++ {
			brand := result.Brands[i]
			fmt.Printf("  - %s", brand.Name)
			if brand.DetailsFetched {
				fmt.Printf(" [✓ Details: %d categories, %d boycott actions, %d alternatives]",
					len(brand.Categories), len(brand.HowToBoycott), len(brand.Alternatives))
			} else {
				fmt.Printf(" [✗ No details: %s]", brand.DetailsError)
			}
			fmt.Println()
		}
		
		if len(result.Brands) > limit {
			fmt.Printf("  ... and %d more\n", len(result.Brands)-limit)
		}
	}
	fmt.Println(strings.Repeat("=", 60))
}