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

function false_negative_expansion_path_php($userPath, $tmp) {
    copy($userPath, '/tmp/out');
    rename($userPath, '/tmp/out');
    move_uploaded_file($tmp, $userPath);
    fopen($userPath, 'r');
    readfile($userPath);
    scandir($userPath);
}
