package main

import "math/rand"

type CrystalStructure struct {
	ID   int
	Name string
}

func NewCrystralStructure(name string) *CrystalStructure {
	return &CrystalStructure{
		ID:   rand.Intn(10000),
		Name: name,
	}
}
