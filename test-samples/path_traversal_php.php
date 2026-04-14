<?php

function read_file($userPath) {
    $content = file_get_contents($userPath);
    include($userPath);
    require($userPath);
}

function write_file($uploadPath, $content) {
    file_put_contents($uploadPath, $content);
}

function delete_file($userPath) {
    unlink($userPath);
}

function concat_path($base, $userPath) {
    return $base . $userPath;
}

function parent_ops($userPath) {
    file_get_contents("../" . $userPath);
    include("../" . $userPath);
    unlink("../" . $userPath);
}
