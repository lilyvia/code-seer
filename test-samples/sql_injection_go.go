package main

import (
	"database/sql"
	"fmt"
)

func vulnerable(db *sql.DB, userID string) {
	db.Query(fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID))
	db.Exec(fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID))
	db.Query("SELECT * FROM users WHERE id = " + userID)
	db.Exec("SELECT * FROM users WHERE id = " + userID)
}

func false_negative_expansion_gorm(db *DB, userID string) {
    userQuery := "SELECT * FROM users WHERE id = " + userID
    db.Raw(userQuery).Scan(&users)
    db.Exec(userQuery)
}
