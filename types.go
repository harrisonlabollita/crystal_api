package main

type Crystal struct {
	Id      int       `json:"id"`
	Name    string    `json:"name"`
	Lattice []float64 `json:"lattice"`
	Volume  float64   `json:"volume"`
	Sgroup  string    `json:"sgroup"`
	Atoms   []string  `json:"atoms"`
	File    string    `json:"file"`
}

func NewCrystral(i int, n string, l []float64, v float64, sg string, a []string,
	f string) *Crystal {
	return &Crystal{Id: i,
		Name:    n,
		Lattice: l,
		Volume:  v,
		Sgroup:  sg,
		Atoms:   a,
		File:    f,
	}

}

type Crystals = []Crystal
