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

func false_negative_expansion_gorm(db *SqliDB, userID string) {
    userQuery := "SELECT * FROM users WHERE id = " + userID
    db.Raw(userQuery).Scan(&users)
    db.Exec(userQuery)
    db.Get(&users, userQuery, userID)
    db.Select(&users, userQuery, userID)
    sqlx.In(userQuery, userID)
    db.QueryRow(fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID), userID)
}

type SqliDB struct{}
type rawQuery struct{}

var users []string
var sqlx sqlxShim

func (db *SqliDB) Raw(query string) *rawQuery { return &rawQuery{} }
func (db *SqliDB) Exec(query string, args ...interface{}) {}
func (db *SqliDB) Get(dest interface{}, query string, args ...interface{}) {}
func (db *SqliDB) Select(dest interface{}, query string, args ...interface{}) {}
func (db *SqliDB) QueryRow(query string, args ...interface{}) {}
func (q *rawQuery) Scan(dest interface{}) {}
func (sqlxShim) In(query string, args ...interface{}) (string, []interface{}, error) { return query, args, nil }

type sqlxShim struct{}
