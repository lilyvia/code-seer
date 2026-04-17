<?php

// Safe: Use json_decode instead of unserialize
function safeLoad($data) {
    $obj = json_decode($data, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception('Invalid JSON');
    }
    return $obj;
}
