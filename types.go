package main

import "math/rand"

type CrystalStructure struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

func NewCrystralStructure(name string) *CrystalStructure {
	return &CrystalStructure{
		ID:   rand.Intn(10000),
		Name: name,
	}
}
