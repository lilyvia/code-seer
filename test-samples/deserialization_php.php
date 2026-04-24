<?php

function parse_payload($userInput, $trustedData) {
    $obj1 = unserialize($userInput);
    $obj2 = unserialize($trustedData, ['allowed_classes' => true]);
    $obj3 = igbinary_unserialize($_POST['data']);
    $obj4 = msgpack_unpack($_POST['data']);
    return [$obj1, $obj2, $obj3, $obj4];
}
