package main

// Match: const apiKey = "..."
const apiKey = "sk1234567890abcdef"

// Match: var apiKey = "..."
var secretKey = "sk1234567890abcdef"

// Match: var password = "..."
var password = "MySecret123"

// Match: var dbPassword = "..."
var dbPassword = "DbPass1234"

// Match: var dsn = "postgres://..."
var dsn = "postgresql://user:pass@localhost/db"

// Match: var awsKey = "AKIA..."
var awsKey = "AKIAIOSFODNN7EXAMPLE"

// Match: var slackToken = "xoxb-..."
var slackToken = "xoxb-123456789012-abcdefghijklmnop"

// Match: var privateKey = "-----BEGIN PRIVATE KEY-----"
var privateKey = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----"

func main() {
	// Match: token := "..." (24+ chars)
	token := "d2hhdGV2ZXI6eW91OnR5cGU6aGVyZQ=="
	_ = token
}
