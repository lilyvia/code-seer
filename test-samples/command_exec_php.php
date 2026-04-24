<?php

function vulnerable_exec($userCmd) {
    exec($userCmd);
}

function vulnerable_system($userCmd) {
    system($userCmd);
}

function vulnerable_shell_exec($userCmd) {
    return shell_exec($userCmd);
}

function safe($userCmd) {
    $allowed = ['whoami', 'date'];
    if (in_array($userCmd, $allowed, true)) {
        return 'allow';
    }
    return '';
}

function false_negative_expansion_php_command($userCmd) {
    proc_open($userCmd, [], $pipes);
    popen($userCmd, 'r');
    pcntl_exec($userCmd, []);
}

function false_negative_expansion_php_backtick($userInput) {
    $backtick = `ls {$userInput}`;
    return $backtick;
}
