<?php

function test_libxml_disable_entity_loader() {
    libxml_disable_entity_loader(false);
}

function test_dom_loadXML_noent($xml) {
    $doc = new DOMDocument();
    $doc->loadXML($xml, LIBXML_NOENT);
}

function test_dom_loadXML_dtdload($xml) {
    $doc = new DOMDocument();
    $doc->loadXML($xml, LIBXML_DTDLOAD);
}

function test_dom_loadXML_dtdattr($xml) {
    $doc = new DOMDocument();
    $doc->loadXML($xml, LIBXML_DTDATTR);
}

function test_simplexml_load_string_noent($xml, $class) {
    simplexml_load_string($xml, $class, LIBXML_NOENT);
}

function test_simplexml_load_string_dtdload($xml, $class) {
    simplexml_load_string($xml, $class, LIBXML_DTDLOAD);
}

function test_simplexml_load_file_noent($xmlFile, $class) {
    simplexml_load_file($xmlFile, $class, LIBXML_NOENT);
}

function test_xmlreader_xml($xml) {
    $reader = new XMLReader();
    $reader->XML($xml);
}

function test_xmlreader_open($xmlPath) {
    $reader = new XMLReader();
    $reader->open($xmlPath);
}
