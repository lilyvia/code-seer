package main

import "html"

// Safe: Escape HTML before output
func safeHTML(userInput string) string {
	escaped := html.EscapeString(userInput)
	return "<div>" + escaped + "</div>"
}

// Safe: Return plain text
func safeText(userInput string) string {
	return userInput
}
