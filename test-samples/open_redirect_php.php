<?php

function vulnerableOpenRedirect($userUrl) {
    header("Location: " . $userUrl);
}

function vulnerableWpRedirect($userUrl) {
    wp_redirect($userUrl);
}

function vulnerableHeaderString($userUrl) {
    header("Location: $userUrl");
}
