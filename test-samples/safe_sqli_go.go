package main

import "database/sql"

// Safe: Use parameterized queries
func getUser(db *sql.DB, userID string) (*sql.Rows, error) {
	return db.Query("SELECT * FROM users WHERE id = ?", userID)
}

func deleteUser(db *sql.DB, id int) (sql.Result, error) {
	return db.Exec("DELETE FROM users WHERE id = ?", id)
}
