# Variables
BINARY_NAME := your_api_name
GO_FILES := $(wildcard *.go)
SQLITE_DB := data.db

# Build the binary
build:
	@go build -o $(BINARY_NAME)

# Run the API
run: build
	@./$(BINARY_NAME)

# Clean the binary and SQLite database
clean:
	@rm -f $(BINARY_NAME)
	@rm -f $(SQLITE_DB)

# Generate JSON files (Add your script command here if you have one)
generate_json:
	@echo "Generating JSON files..."

# Generate and initialize the SQLite database (Add your script command here if you have one)
generate_database:
	@echo "Generating and initializing the SQLite database..."

# Build and run the API with JSON and database generation
build_and_run: generate_json generate_database run

# Show help
help:
	@echo "Available targets:"
	@echo "  build          - Build the binary"
	@echo "  run            - Run the API"
	@echo "  clean          - Clean up generated files"
	@echo "  generate_json  - Generate JSON files"
	@echo "  generate_database - Generate and initialize the SQLite database"
	@echo "  build_and_run  - Build and run the API with JSON and database generation"
	@echo "  help           - Show this help message"
