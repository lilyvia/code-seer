package main

import "net/http"

// Safe: Check user ownership before returning resources
func getOrder(w http.ResponseWriter, r *http.Request) {
	orderID := r.URL.Query().Get("id")
	order := orderRepo.GetOrderByID(orderID)
	uid := r.Header.Get("X-User-ID")
	if order.UserID != uid {
		w.WriteHeader(http.StatusForbidden)
		return
	}
	w.Write([]byte(order.JSON()))
}

// Safe: Admin route with middleware
func adminOnly(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if !isAdmin(r) {
			w.WriteHeader(http.StatusForbidden)
			return
		}
		next(w, r)
	}
}

func registerSafeAdminRoutes(r *Router, app *FiberApp) {
	admin := r.Group("/admin", AuthMiddleware())
	admin.Delete("/users/:id", deleteAdminUser)
	app.Use(AuthMiddleware())
	app.Delete("/secure/users/:id", deleteAdminUser)
}
