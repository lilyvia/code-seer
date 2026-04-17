<?php

class SafePrototypePollutionPhp {
    private $allowedProperties = ['name', 'email', 'age'];

    public function safeDynamicProperty($obj, $propertyName, $value) {
        if (in_array($propertyName, $this->allowedProperties)) {
            $obj->setProperty($propertyName, $value);
        }
    }

    public function safeDeserialize($userInput) {
        return json_decode($userInput, true);
    }
}
