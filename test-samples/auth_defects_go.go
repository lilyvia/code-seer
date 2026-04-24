package main

import (
	"net/http"
)

// Minimal stub types so the file parses as valid Go without external deps.
type Context struct{}

func (c *Context) Param(key string) string     { return "" }
func (c *Context) Query(key string) string     { return "" }
func (c *Context) JSON(code int, obj any)      {}
func (c *Context) GetString(key string) string { return "" }
func (c *Context) AbortWithStatus(code int)    {}

type DB struct{}

func (db *DB) Find(dest any, conds ...any) *DB     { return db }
func (db *DB) First(dest any, conds ...any) *DB    { return db }
func (db *DB) Where(query string, args ...any) *DB { return db }

var gdb *DB

type Order struct {
	ID     int
	UserID string
}

type User struct {
	ID   int
	Name string
}

type Product struct{}

// Pattern 1: IDOR - Direct database lookup from URL parameter without ownership check
func getOrder(w http.ResponseWriter, r *http.Request) {
	order, _ := repo.GetOrderByID(r.URL.Query().Get("order_id"))
	w.Write([]byte(order.UserID))
}

// Pattern 1 variant: Gin param direct lookup
func getUserGin(c *Context) {
	user, err := userDB.FindByID(c.Param("id"))
	if err != nil {
		c.JSON(500, map[string]string{"error": err.Error()})
		return
	}
	c.JSON(200, user)
}

// Pattern 2: Delete operation with only authentication check
func deleteUserHandler(w http.ResponseWriter, r *http.Request) {
	userID := r.URL.Query().Get("user_id")
	id := r.URL.Query().Get("id")
	if userID != "" {
		repo.DeleteUser(id)
	}
}

// Pattern 3: Direct query from request parameter (GORM style)
func getProduct(c *Context) {
	var model Product
	result := gdb.First(&model, c.Query("id"))
	c.JSON(200, result)
}

// Pattern 3 variant: Where clause with request param
func getOrderWhere(c *Context) {
	var order Order
	gdb.Where("id = ?", c.Param("order_id")).First(&order)
	c.JSON(200, order)
}

// Pattern 4: Direct return of database lookup
func findUserDirect(c *Context) {
	c.JSON(http.StatusOK, gdb.Find(c.Param("id")))
}

// Helpers
var repo = &Repository{}
var userDB = &UserDB{}

type Repository struct{}

func (r *Repository) GetOrderByID(id string) (*Order, error) {
	return nil, nil
}

func (r *Repository) DeleteUser(id string) error {
	return nil
}

type UserDB struct{}

func (u *UserDB) FindByID(id string) (*User, error) {
	return nil, nil
}

func registerInsecureAdminRoutes(r *Router, app *FiberApp) {
	admin := r.Group("/admin")
	admin.Delete("/users/:id", deleteAdminUser)
	app.Delete("/admin/users/:id", deleteAdminUser)
}
