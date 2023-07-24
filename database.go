package main

import (
	"database/sql",
	"encoding/json",
	"fmt",
	"io/ioutil",
	"os",
	"path/filepath",

	"github.com/mattn/go-sqlite3"
)


type Database struct {
	db sql.DB
}

func NewDatabase(name string) *sql.DB {
	db, err := sql.Open("sqlite3", name)
	if err != nil {
		fmt.Println("Error opending database")
	}
	return  &Database {
		db : db,
	}
}


func Build(name string) {

	db, err := sql.Open("sqlite3", name)
	if err != nil {
		fmt.Prinln("Error opening database ", err)
	}

	defer db.Close()

	_, err = db.Exec(`
	   CREATE TABLE IF NOT EXISTS crystals (
		id INTEGER PRIMARY KEY
		name TEXT
		lattice FLOAT[]
		volume FLOAT
		sgroup TEXT
		atoms  TEXT
		file   TEXT
	   )`)

	if err != nil {
		fmt.Println("Error creating table: ", err)
		return 
	}


	var dataFolder string = "/data/"
	fileList, err := ioutil.ReadDir(dataFolder)
	if err != nil {
		fmt.Println("Error reading data folder: ", err)
		return 
	}

	for _, file := range fileList {
		if !file.IsDir() && filepath.Ext(file.Name()) == ".json" {
			// read the Json file
			content, err := ioutil.ReadFile(filepath.Join(dataFolder, file.Name()))
			if err != nil {
				fmt.Println("Error reading JSON file: ", err)
				continue
			}

			var crystal Crystal
			err = json.Unmarshal(content, &crystal)
			if err != nil {
				fmt.Println("Error parsing JSON file: ", err)
				continue
			}

			_, err = db.Exec("INSERT INTO crystals (id, name, lattice, volume, sgroup, atoms, file) VALUES (?, ?, ?, ?, ?, ?, ?)", 
			crystal.Id,
			crystal.Name,
			crystal.Lattice,
			crystal.Sgroup,
			crystal.Atoms,
			crystal.File
		)
		}
	}
}