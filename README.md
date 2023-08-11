# CrystalAPI

CrystalAPI is a Flask-based API that provides access to a materials database. It allows you to retrieve materials by ID, name, or apply various filters for querying materials based on volume, atom composition, and space group.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [Database](#database)
- [Contributing](#contributing)

## Features

- Retrieve materials by ID or name.
- Query materials with filters like volume, atom composition, and space group.
- SQLite-based database for efficient data storage and retrieval.
- JSON formatted responses for easy consumption.

## Installation


   ```bash
   git clone https://github.com/harrisonlabollita/crystal_api.git
   cd crystal_api
   ```

## Usage

1. Install Flask dependencies.
2. run app (``python3 app.py``)
3. The API will run on your local host ``http://localhost:5000``.


## Routes

- ``GET /material/<int:material_id>``: Get a material by its ID.
- ``GET /material/<name>``: Get a material by its name.
- ``GET /materials/``:  Query materials based on filters.

## Database

The materials data is stored in an SQLite database located at ``data/database.db``. The schema of the materials table includes columns for ``id``, ``name``, ``lattice``, ``volume``, ``atoms``, ``sgroup``, and  ``source``.

## Contributing

Contributions are welcome! Here's how you can get involved:

1. Fork the repository.
2. Create a new branch: ``git checkout -b feature-new-feature``.
3. Make your changes and commit them: ``git commit -m 'Add new feature'``.
4. Push to the branch: ``git push origin feature-new-feature``.
5. Create a pull request detailing your changes.


## Reference
Downs, R.T. and Hall-Wallace, M. (2003) The American Mineralogist Crystal Structure Database. [American Mineralogist 88, 247-250](https://rruff.info/xtal/group/pdf/am88_247.pdf).
