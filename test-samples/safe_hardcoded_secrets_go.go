package main

import "os"

// Safe: Read secrets from environment variables
func getAPIKey() string {
	return os.Getenv("API_KEY")
}

func getDBPassword() string {
	return os.Getenv("DB_PASSWORD")
}

func getServiceTokens() (string, string, string) {
	return os.Getenv("OPENAI_API_KEY"), os.Getenv("GOOGLE_API_KEY"), os.Getenv("MONGODB_URI")
}

// Safe: Reference to secret manager
func secretFromVault(name string) string {
	return "vault://" + name
}
