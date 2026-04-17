package main

import "encoding/json"

// Safe: Use json.Unmarshal with struct binding
type User struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

func safeParse(data []byte) (*User, error) {
	var u User
	if err := json.Unmarshal(data, &u); err != nil {
		return nil, err
	}
	return &u, nil
}
