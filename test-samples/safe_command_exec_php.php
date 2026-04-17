<?php

// Safe: Use PHP built-in functions instead of shell commands
function safeListFiles($dir) {
    return scandir($dir);
}

// Safe: Use PHP native functions for file operations
function safeFileInfo($path) {
    return pathinfo($path);
}
