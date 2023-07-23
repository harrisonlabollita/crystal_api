package main

import "database/sql"

type Storage interface {
	CreateCrystal(*CrystalStructure) error
	DeleteCrystal(int) error
	GetCrystalByID(int) (*CrystalStructure, error)
}

type PostgresStore struct {
	db *sql.DB
}

func NewPostgressStore() (*PostgresStore, error) {

}
