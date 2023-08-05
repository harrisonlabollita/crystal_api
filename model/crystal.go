package model

type Crystal struct {
    ID        int       `json:"id"`
    Name      string    `json:"name"`
    Lattice   []float64 `json:"lattice"`
    Sgroup    string    `json:"sgroup"`
    Atoms     string    `json:"atoms"`
    File      string    `json:"file"`
}
