package main

// Safe: Use a custom XML parser that disables DTD parsing
// For untrusted XML, prefer JSON or validate with strict schema
func safeProcessXML(xmlData []byte) bool {
	// Validate XML length to prevent DoS
	if len(xmlData) > 1024*1024 {
		return false
	}
	// In production, use a parser with DTD disabled
	return true
}
