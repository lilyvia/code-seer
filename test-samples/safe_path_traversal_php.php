<?php

// Safe: Validate user path using sprintf
function safePath($baseDir, $userPath) {
    $base = realpath($baseDir);
    $target = realpath(sprintf('%s/%s', $base, $userPath));
    if ($target === false || strpos($target, sprintf('%s/', $base)) !== 0) {
        throw new Exception('Path traversal detected');
    }
    return $target;
}
