<?php

// Safe: Validate URL against allowlist
function isSafeUrl($url) {
    $allowedHosts = ['api.example.com', 'files.example.com'];
    $parsed = parse_url($url);
    return isset($parsed['scheme']) && $parsed['scheme'] === 'https'
        && isset($parsed['host']) && in_array($parsed['host'], $allowedHosts, true);
}

function safeFetch($url) {
    if (!isSafeUrl($url)) {
        throw new Exception('URL not allowed');
    }
    // In production, use a dedicated HTTP client with timeout
    return 'fetching ' . $url;
}

function safeGuzzleFetch($client, $url) {
    if (!isSafeUrl($url)) {
        throw new Exception('URL not allowed');
    }
    return $client->send(new Request('GET', $url));
}
