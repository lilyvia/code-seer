<?php

function parse_payload($userInput, $trustedData) {
    $obj1 = unserialize($userInput);
    $obj2 = unserialize($trustedData, ['allowed_classes' => true]);
    return [$obj1, $obj2];
}
