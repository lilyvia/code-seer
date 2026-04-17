package main

import "os"

// Safe: Read secrets from environment variables
func getAPIKey() string {
	return os.Getenv("API_KEY")
}

func getDBPassword() string {
	return os.Getenv("DB_PASSWORD")
}

// Safe: Reference to secret manager
func secretFromVault(name string) string {
	return "vault://" + name
}
