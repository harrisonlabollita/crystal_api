package main

func main() {
	port := ":3000"

    database := BuildCrystalData()

	server := NewAPIServer(port, database)

	server.Run()
}
