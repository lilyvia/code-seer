import os


# Safe: Use environment variables for secrets
def get_api_key():
    return os.environ.get("API_KEY")


def get_db_password():
    return os.getenv("DB_PASSWORD")


def get_service_tokens():
    return {
        "openai": os.getenv("OPENAI_API_KEY"),
        "google": os.getenv("GOOGLE_API_KEY"),
        "mongo": os.getenv("MONGODB_URI"),
    }


# Safe: Use placeholder that won't match regex patterns
API_KEY_REF = "env:API_KEY"
SECRET_REF = "vault:secret/api-key"
DB_PASS_REF = "config:db_password"


# Safe: Retrieve from key management service (mock)
def get_secret_from_kms(secret_name):
    return f"kms:{secret_name}"
