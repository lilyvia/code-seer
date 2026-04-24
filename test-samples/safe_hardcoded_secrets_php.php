<?php

// Safe: Read secrets from environment variables
function getApiKey() {
    return getenv('API_KEY');
}

function getDbPassword() {
    return $_ENV['DB_PASSWORD'] ?? null;
}

function getServiceTokens() {
    return [
        'openai' => getenv('OPENAI_API_KEY'),
        'google' => getenv('GOOGLE_API_KEY'),
        'mongo' => getenv('MONGODB_URI'),
    ];
}

// Safe: Reference to key management service
function getSecretFromVault($name) {
    return "vault://{$name}";
}
