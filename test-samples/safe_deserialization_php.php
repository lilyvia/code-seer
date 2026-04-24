<?php

// Safe: Use json_decode instead of unserialize
function safeLoad($data) {
    $obj = json_decode($data, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception('Invalid JSON');
    }
    return $obj;
}

function safeUnserializeWithHmac($payload, $signature, $key) {
    $expected = hash_hmac('sha256', $payload, $key);
    if (!hash_equals($expected, $signature)) {
        throw new Exception('Invalid signature');
    }
    return \unserialize($payload, ['allowed_classes' => ['SafeDto']]);
}

class SafeDto {}
