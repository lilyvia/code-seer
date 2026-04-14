# Python hardcoded secrets test samples

# Match: api_key = "..." (12+ chars alphanumeric)
api_key = "sk1234567890abcdef"

# Match: password = "..." (6+ chars)
password = "MySecret123"

# Match: db_password = "..." (8+ chars)
db_password = "DbPass1234"

# Match: database_url = "..."
database_url = "postgresql://user:pass@localhost/db"

# Match: AKIA[0-9A-Z]{16} (AWS key)
aws_access_key = "AKIAIOSFODNN7EXAMPLE"

# Match: xoxb-... (Slack token)
slack_token = "xoxb-123456789012-abcdefghijklmnop"

# Match: ghp_... (GitHub token)
github_token = "ghp_1234567890abcdefghijklmnopqrst"

# Match: sk_live_... (Stripe key)
stripe_key = "sk_live_1234567890abcdef12345678"

# Match: -----BEGIN PRIVATE KEY-----
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----"

# Match: token = "..." (24+ chars base64-like)
token = "d2hhdGV2ZXI6eW91OnR5cGU6aGVyZQ=="
