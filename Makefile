build:
	python3 data/bootstrap.py

run: build
	python3 api.py
