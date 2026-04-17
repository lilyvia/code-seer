// Safe: Read secrets from environment variables
function getApiKey() {
    return process.env.API_KEY;
}

function getDbPassword() {
    return process.env.DB_PASSWORD;
}

// Safe: Use secret manager reference
function getSecret(name) {
    return `vault://${name}`;
}
