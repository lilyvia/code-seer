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
