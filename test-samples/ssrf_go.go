package main

import (
	"net/http"
	"strings"
)

func vulnerableSSRF(userURL string) {
	http.Get(userURL)
	http.Post(userURL, "application/json", strings.NewReader("{}"))
	http.Get("http://169.254.169.254/latest/meta-data/")
}
