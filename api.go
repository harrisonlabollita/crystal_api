package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func WriteJSON(w http.ResponseWriter, status int, v any) error {
	w.WriteHeader(status)
	w.Header().Set("Content-Type", "application/json")
	return json.NewEncoder(w).Encode(v)
}

type ApiFunc func(http.ResponseWriter, *http.Request) error

type ApiError struct {
	Error string
}

func MakeHTTPHandleFunc(f ApiFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if err := f(w, r); err != nil {
			WriteJSON(w, http.StatusBadRequest, ApiError{Error: err.Error()})
		}
	}
}

// API Server
type APIServer struct {
	listenAddr string
}

func NewAPIServer(listenAddr string) *APIServer {
	return &APIServer{
		listenAddr: listenAddr,
	}
}

func (s *APIServer) Run() {
	router := mux.NewRouter()
	router.HandleFunc("/crystal", MakeHTTPHandleFunc(s.HandleCrystal))
	log.Println("server rungin on port: ", s.listenAddr)
	http.ListenAndServe(s.listenAddr, router)
}

// http Handlers
func (s *APIServer) HandleCrystal(w http.ResponseWriter, r *http.Request) error {
	if r.Method == "GET" {
		return s.HandleGetCrystal(w, r)
	}
	if r.Method == "POST" {
		return s.HandleCreateCrystal(w, r)
	}
	if r.Method == "DELETE" {
		return s.HandleDeleteCrystal(w, r)
	}
	return fmt.Errorf("method not allowed %s", r.Method)
}

func (s *APIServer) HandleGetCrystal(w http.ResponseWriter, r *http.Request) error {
	test := NewCrystralStructure("TestMineral")
	return WriteJSON(w, http.StatusOK, test)
}

func (s *APIServer) HandleCreateCrystal(w http.ResponseWriter, r *http.Request) error {
	return nil
}

func (s *APIServer) HandleDeleteCrystal(w http.ResponseWriter, r *http.Request) error {
	return nil
}
