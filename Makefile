build:
	@go build -o bin/mineralapi

run: build
	@./bin/mineralapi

test:
	@go test -v ./...
