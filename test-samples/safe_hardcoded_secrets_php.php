<?php

// Safe: Read secrets from environment variables
function getApiKey() {
    return getenv('API_KEY');
}

function getDbPassword() {
    return $_ENV['DB_PASSWORD'] ?? null;
}

// Safe: Reference to key management service
function getSecretFromVault($name) {
    return "vault://{$name}";
}
