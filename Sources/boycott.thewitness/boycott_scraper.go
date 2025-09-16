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

// Brand represents a boycott target brand
type Brand struct {
	Name        string    `json:"name"`
	ImageURL    string    `json:"image_url"`
	TargetLink  string    `json:"target_link"`
	PageNumber  int       `json:"page_number"`
	ScrapedAt   time.Time `json:"scraped_at"`
}

// ScrapeResult holds all scraped data
type ScrapeResult struct {
	TotalBrands   int       `json:"total_brands"`
	TotalPages    int       `json:"total_pages"`
	Brands        []Brand   `json:"brands"`
	ScrapedAt     time.Time `json:"scraped_at"`
	LastPageEmpty bool      `json:"last_page_empty"`
}

func main() {
	log.Println("Starting Boycott The Witness scraper...")

	// Get output directory from environment or use default
	outputDir := os.Getenv("OUTPUT_DIR")
	if outputDir == "" {
		outputDir = "/output"
	}

	// Ensure output directory exists
	err := os.MkdirAll(outputDir, 0755)
	if err != nil {
		log.Fatalf("Failed to create output directory: %v", err)
	}

	result := ScrapeResult{
		Brands:    []Brand{},
		ScrapedAt: time.Now(),
	}

	baseURL := "https://boycott.thewitness.news/browse/"
	pageNumber := 1
	emptyPageCount := 0
	maxEmptyPages := 3 // Stop after 3 consecutive empty pages

	log.Println("Starting to scrape pages...")

	for {
		log.Printf("Scraping page %d...", pageNumber)
		
		brands, err := scrapePage(fmt.Sprintf("%s%d", baseURL, pageNumber))
		if err != nil {
			log.Printf("Error scraping page %d: %v", pageNumber, err)
			emptyPageCount++
			
			if emptyPageCount >= maxEmptyPages {
				log.Printf("Reached %d consecutive empty pages, stopping...", maxEmptyPages)
				result.LastPageEmpty = true
				break
			}
			
			pageNumber++
			time.Sleep(1 * time.Second)
			continue
		}

		if len(brands) == 0 {
			emptyPageCount++
			log.Printf("Page %d returned no brands (empty page count: %d)", pageNumber, emptyPageCount)
			
			if emptyPageCount >= maxEmptyPages {
				log.Printf("Reached %d consecutive empty pages, stopping...", maxEmptyPages)
				result.LastPageEmpty = true
				break
			}
		} else {
			emptyPageCount = 0 // Reset counter on successful page
			log.Printf("Found %d brands on page %d", len(brands), pageNumber)
			
			// Add page number to each brand
			for i := range brands {
				brands[i].PageNumber = pageNumber
			}
			
			result.Brands = append(result.Brands, brands...)
		}

		pageNumber++
		
		// Be respectful with rate limiting
		time.Sleep(1 * time.Second)
		
		// Safety limit to prevent infinite loops
		if pageNumber > 100 {
			log.Println("Reached maximum page limit (100), stopping...")
			break
		}
	}

	result.TotalPages = pageNumber - 1
	result.TotalBrands = len(result.Brands)

	// Save results to JSON
	timestamp := time.Now().Format("20060102_150405")
	outputFile := filepath.Join(outputDir, fmt.Sprintf("boycott_brands_%s.json", timestamp))
	
	jsonData, err := json.MarshalIndent(result, "", "  ")
	if err != nil {
		log.Fatalf("Failed to marshal JSON: %v", err)
	}

	err = os.WriteFile(outputFile, jsonData, 0644)
	if err != nil {
		log.Fatalf("Failed to write JSON file: %v", err)
	}

	// Also save a "latest" version
	latestFile := filepath.Join(outputDir, "boycott_brands_latest.json")
	err = os.WriteFile(latestFile, jsonData, 0644)
	if err != nil {
		log.Printf("Failed to write latest file: %v", err)
	}

	// Create a CSV file for easy viewing
	csvFile := filepath.Join(outputDir, fmt.Sprintf("boycott_brands_%s.csv", timestamp))
	err = writeCSV(csvFile, result.Brands)
	if err != nil {
		log.Printf("Failed to write CSV file: %v", err)
	}

	// Print summary
	fmt.Println("\n" + strings.Repeat("=", 50))
	fmt.Printf("Scraping complete!\n")
	fmt.Printf("Total pages scraped: %d\n", result.TotalPages)
	fmt.Printf("Total brands found: %d\n", result.TotalBrands)
	fmt.Printf("Results saved to: %s\n", outputFile)
	
	if result.TotalBrands > 0 {
		fmt.Println("\nSample of brands found:")
		limit := 10
		if len(result.Brands) < limit {
			limit = len(result.Brands)
		}
		for i := 0; i < limit; i++ {
			fmt.Printf("  - %s (page %d)\n", result.Brands[i].Name, result.Brands[i].PageNumber)
		}
		if len(result.Brands) > 10 {
			fmt.Printf("  ... and %d more\n", len(result.Brands)-10)
		}
	}
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

	// Look for brand cards - they have a specific structure
	doc.Find("div.m-e615b15f.mantine-Card-root").Each(func(i int, s *goquery.Selection) {
		// Skip the first card if it's the featured news card
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
			}
		}

		// Only add if we found a name
		if brand.Name != "" && brand.Name != "Featured news" {
			brands = append(brands, brand)
		}
	})

	// Alternative selector if the first one doesn't work
	if len(brands) == 0 {
		// Try a more general approach
		doc.Find("a[href^='/target/']").Each(func(i int, s *goquery.Selection) {
			href, _ := s.Attr("href")
			
			// Find the parent card
			card := s.ParentsFiltered("div.mantine-Card-root").First()
			if card.Length() > 0 {
				brand := Brand{
					ScrapedAt:  time.Now(),
					TargetLink: href,
				}
				
				// Extract name from the card
				nameElem := card.Find("p[data-size='lg']")
				if nameElem.Length() > 0 {
					brand.Name = strings.TrimSpace(nameElem.Text())
				}
				
				// Extract image
				imgElem := card.Find("img").First()
				if imgElem.Length() > 0 {
					brand.ImageURL, _ = imgElem.Attr("src")
				}
				
				if brand.Name != "" {
					// Check if already added
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

func writeCSV(filename string, brands []Brand) error {
	file, err := os.Create(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	// Write header
	fmt.Fprintln(file, "Name,Target Link,Image URL,Page Number,Scraped At")

	// Write data
	for _, brand := range brands {
		// Escape commas in fields
		name := strings.ReplaceAll(brand.Name, ",", ";")
		imageURL := strings.ReplaceAll(brand.ImageURL, ",", ";")
		
		fmt.Fprintf(file, "%s,%s,%s,%d,%s\n",
			name,
			brand.TargetLink,
			imageURL,
			brand.PageNumber,
			brand.ScrapedAt.Format(time.RFC3339),
		)
	}

	return nil
}