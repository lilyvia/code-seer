<?php
$userInput = $_GET['input'];

// Vulnerable: echo $USER_INPUT (not wrapped in htmlspecialchars)
echo $userInput;

// Vulnerable: print $USER_INPUT (not wrapped in htmlspecialchars)
print $userInput;

// Safe: wrapped in htmlspecialchars - should NOT match
echo htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');

// Safe: wrapped in htmlspecialchars - should NOT match
print htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');

function false_negative_expansion_xss_php($userInput) {
    echo $userInput;
    print $userInput;
}
