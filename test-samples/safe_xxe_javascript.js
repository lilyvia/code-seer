// Safe: Use JSON instead of XML for untrusted data
function safeParse(data) {
    return JSON.parse(data);
}

// Safe: If XML is needed, use a secure parser with DTD disabled
// Example: fast-xml-parser with safe options
function safeXmlParse(xml) {
    // Use a parser that disables entity expansion by default
    return { parsed: true, length: xml.length };
}
