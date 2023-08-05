package database

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

const rawFileURL = "https://example.com/cifdata.txt" //TODO : replace
const rawFile = "cifdata.txt"

func downloadRawFile() error {
	fmt.Println("Downloading the raw file...")
	resp, err := http.Get(rawFileURL)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	file, err := os.Create(rawFile)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		return err
	}

	fmt.Println("Download completed successfully.")
	return nil
}

func buildDatabase() {
	_, err := os.Stat(rawFile)

	if os.IsNotExist(err) {
		err = downloadRawFile()
		if err != nil {
			fmt.Println("Error downloading the raw file:", err)
			return
		}
	}

	file, err := os.Open(rawFile)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)

	var ciffile []string
	var numid int = 10000
	var name, sgroup, species string
	var a, b, c, alpha, beta, gamma, volume float64

	for scanner.Scan() {

		line := scanner.Text()

		if strings.Contains(line, "END") {
			ciffile = append(ciffile, line)

			Crystal := make(map[string]interface{})
			Crystal["id"] = numid
			Crystal["name"] = name
			Crystal["lattice"] = []float64{a, b, c, alpha, beta, gamma}
			Crystal["volume"] = volume
			Crystal["sgroup"] = sgroup
			Crystal["atoms"] = species
			Crystal["file"] = strings.Join(ciffile, "\n")

			jsonFile, err := os.Create(strconv.Itoa(Crystal["id"].(int)) + ".json")
			if err != nil {
				fmt.Println("Error creating JSON file:", err)
				return
			}
			defer jsonFile.Close()

			encoder := json.NewEncoder(jsonFile)
			encoder.SetIndent("", "    ")
			if err := encoder.Encode(Crystal); err != nil {
				fmt.Println("Error writing JSON:", err)
			}
			numid++
			ciffile = nil

		} else {

			ciffile = append(ciffile, line)

			if strings.Contains(line, "chemical_name_mineral") {
				name = strings.TrimSpace(strings.Split(line, "_chemical_name_mineral")[-1])
			}
			if strings.Contains(line, "cell_length_a") {
				a, _ = strconv.ParseFloat(strings.TrimSpace(strings.Split(line, " ")[-1]), 64)
			}
			if strings.Contains(line, "cell_length_b") {
				b, _ = strconv.ParseFloat(strings.TrimSpace(strings.Split(line, " ")[-1]), 64)
			}
			if strings.Contains(line, "cell_length_c") {
				c, _ = strconv.ParseFloat(strings.TrimSpace(strings.Split(line, " ")[-1]), 64)
			}
			if strings.Contains(line, "cell_angle_alpha") {
				alpha, _ = strconv.ParseFloat(strings.TrimSpace(strings.Split(line, " ")[-1]), 64)
			}
			if strings.Contains(line, "cell_angle_beta") {
				beta, _ = strconv.ParseFloat(strings.TrimSpace(strings.Split(line, " ")[-1]), 64)
			}
			if strings.Contains(line, "cell_angle_gamma") {
				gamma, _ = strconv.ParseFloat(strings.TrimSpace(strings.Split(line, " ")[-1]), 64)
			}
			if strings.Contains(line, "cell_volume") {
				volume, _ = strconv.ParseFloat(strings.TrimSpace(strings.Split(line, " ")[-1]), 64)
			}
			if strings.Contains(line, "symmetry_space_group_name") {
				sgroup = strings.TrimSpace(strings.Split(line, "symmetry_space_group_name_H-M")[-1])
				sgroup = strings.ReplaceAll(sgroup, ",", "")
				sgroup = strings.ReplaceAll(sgroup, " ", "")
				sgroup = strings.ReplaceAll(sgroup, "'", "")
			}
			if strings.Contains(line, "chemical_formula_sum") {
				line = strings.ReplaceAll(line, "(", "")
				line = strings.ReplaceAll(line, ")", "")
				line = strings.ReplaceAll(line, "'", "")
				speciesList := strings.Fields(line)
				var modifiedSpecies []string
				for _, s := range speciesList[1:] {
					for _, c := range s {
						if !unicode.IsDigit(c) {
							modifiedSpecies = append(modifiedSpecies, string(c))
						}
					}
				}
				species = strings.Join(modifiedSpecies, " ")
			}
		}
	}
}
