package main

import "database/sql"

// Safe: Use parameterized queries
func getUser(db *sql.DB, userID string) (*sql.Rows, error) {
	return db.Query("SELECT * FROM users WHERE id = ?", userID)
}

func deleteUser(db *sql.DB, id int) (sql.Result, error) {
	return db.Exec("DELETE FROM users WHERE id = ?", id)
}

func safeSqlxGet(db *SafeDB, id string) error {
	return db.Get(&safeData, "SELECT * FROM accounts WHERE id = ?", id)
}

type SafeDB struct{}

var safeData []string

func (db *SafeDB) Get(dest interface{}, query string, args ...interface{}) error { return nil }
