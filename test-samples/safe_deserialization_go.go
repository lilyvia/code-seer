package main

import (
	"bytes"
	"encoding/gob"
	"encoding/json"
	"fmt"
)

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

func safeGobDecodeWithValidation(data []byte) (*User, error) {
	var u User
	decoder := gob.NewDecoder(bytes.NewReader(data))
	if err := decoder.Decode(&u); err != nil {
		return nil, err
	}
	if u.Name == "" || u.Age < 0 || u.Age > 130 {
		return nil, fmt.Errorf("invalid user")
	}
	return &u, nil
}
