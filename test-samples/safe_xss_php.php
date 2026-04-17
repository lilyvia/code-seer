<?php

// Safe: Escape HTML output
function safeOutput($userInput) {
    return htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');
}

// Safe: Use template engine auto-escaping
function renderPage($name) {
    return "<div>" . htmlentities($name, ENT_QUOTES, 'UTF-8') . "</div>";
}
