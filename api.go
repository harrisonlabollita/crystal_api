package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

// API Server
type APIServer struct {
	listenAddr string
    database Crystals
}

func NewAPIServer(listenAddr string, database Crystals) *APIServer {
	return &APIServer{
		listenAddr: listenAddr,
        database: database,
	}
}

func (s *APIServer) Run() {
	router := mux.NewRouter()

	router.HandleFunc("/crystals", s.GetCrystalHandler).Methods("GET")

	log.Println("server running on port: ", s.listenAddr)
	http.ListenAndServe(s.listenAddr, router)
}

// Handlers

// Handle function to handle GET requests and filtering of the database
func (s *APIServer) GetCrystalHandler(w http.ResponseWriter, r *http.Request ) {

    query := r.URL.Query()

    crystals := filterCrystals(s.database, query)

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(crystals)
}
