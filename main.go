package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

type CrystalStructure struct {
	// Define the structure of your JSON crystal structure
	// For example:
	// ID             int    `json:"id"`
	// Name           string `json:"name"`
	// SpaceGroup     int    `json:"spacegroup"`
	// SpaceGroupName int    `json:"spacegroupname"`
	// AtomicSpecies  []string
}

// Define a function to read the JSON data from files
func readData() ([]CrystalStructure, error) {
	var structures []CrystalStructure

	dataDir := "./data"
	err := filepath.Walk(dataDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() && strings.HasSuffix(info.Name(), ".json") {
			file, err := os.Open(path)
			if err != nil {
				return err
			}
			defer file.Close()

			var structure CrystalStructure
			err = json.NewDecoder(file).Decode(&record)
			if err != nil {
				return err
			}
			structures = append(structures, structure)
		}
		return nil
	})
	return structure, err
}

// Define a function to handle the GET requests and filtering criteria
func handleGetRequest(w http.ResponseWriter, r *http.Request) {
	// Get the filtering criteria from query parameters
	queryParams := r.URL.Query()

	// Filter the data based on queryParams and your logic
	// For example:
	// filteredRecords := filterDataBasedOnQueryParams(records, queryParams)

	// Return the filtered records as JSON response
	// json.NewEncoder(w).Encode(filteredRecords)
}

func main() {
	// Read the JSON data from files
	records, err := readData()
	if err != nil {
		log.Fatalf("Error reading data: %v", err)
	}

	// Define the endpoint for GET requests
	http.HandleFunc("/api/getdata", handleGetRequest)

	// Start the server on port 8080
	port := "8080"
	fmt.Printf("Server started on http://localhost:%s\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
