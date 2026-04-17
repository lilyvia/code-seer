<?php

function safeRedirect($target) {
    $allowedHosts = ['example.com'];
    $parsed = parse_url($target);
    if (isset($parsed['host']) && !in_array($parsed['host'], $allowedHosts, true)) {
        throw new Exception('非法跳转目标');
    }
    return $target;
}

function safeOpenRedirect($userUrl) {
    $safe = safeRedirect($userUrl);
    header("Location: " . $safe);
}

function safeHardcodedRedirect() {
    header("Location: /dashboard");
}

function safeWpRedirect() {
    wp_safe_redirect("/dashboard");
}
