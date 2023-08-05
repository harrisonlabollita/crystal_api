package database

import (
    "database/sql"
    "github.com/mattn/go-sqlite3"
)

func InitSQLDatabase() (*sql.DB, error) {

    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        return nil, err
    }

    _, err = db.Exec(`
        CREATE TABLE IF NOT EXISTS crystals (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            lattice FLOAT NOT NULL,
            sgroup TEXT NOT NULL,
            atoms TEXT NOT NULL,
            file TEXT NOT NULL
        )
    `)
    if err != nil {
        return nil, err
    }

    return db, nil
}
