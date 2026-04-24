// Safe: Read secrets from environment variables
function getApiKey() {
    return process.env.API_KEY;
}

function getDbPassword() {
    return process.env.DB_PASSWORD;
}

function getServiceTokens() {
    return {
        openai: process.env.OPENAI_API_KEY,
        google: process.env.GOOGLE_API_KEY,
        mongo: process.env.MONGODB_URI,
    };
}

// Safe: Use secret manager reference
function getSecret(name) {
    return `vault://${name}`;
}
