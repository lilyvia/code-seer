<?php

// Safe: Disable external entities and network access
function safeLoadXML($xml) {
    $doc = new DOMDocument();
    $doc->resolveExternals = false;
    $doc->substituteEntities = false;
    $doc->loadXML($xml, LIBXML_NONET);
    return $doc;
}

// Safe: Use simplexml with safe options
function safeSimpleXML($xml) {
    return simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NONET);
}

function safeSimpleXMLWithOptions($xml) {
    return simplexml_load_string($xml, 'SimpleXMLElement', LIBXML_NONET | LIBXML_NOCDATA);
}
