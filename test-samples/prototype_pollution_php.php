<?php

class PrototypePollutionPhp {
    public function vulnerableDynamicProperty($obj, $userProperty, $userValue) {
        $obj->$userProperty = $userValue;
    }

    public function vulnerableUnserialize($userInput) {
        return unserialize($userInput);
    }

    public function vulnerableDynamicPropertyDirect($obj, $userProperty, $userValue) {
        $property = $userProperty;
        $obj->$property = $userValue;
    }
}
