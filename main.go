package main

func main() {
	port := ":3000"
	server := NewAPIServer(port)
	server.Run()
}
