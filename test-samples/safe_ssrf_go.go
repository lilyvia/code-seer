package main

import (
	"fmt"
	"net/url"
)

var allowedHosts = map[string]bool{"api.example.com": true, "files.example.com": true}

// Safe: Validate URL before fetching
func safeFetch(target string) (string, error) {
	u, err := url.Parse(target)
	if err != nil {
		return "", err
	}
	if u.Scheme != "https" || !allowedHosts[u.Host] {
		return "", fmt.Errorf("untrusted url")
	}
	return fmt.Sprintf("fetching %s", target), nil
}

func safeRestyFetch(client *safeRestyClient) {
	client.R().Get("https://api.example.com/status")
}

type safeRestyClient struct{}
type safeRestyRequest struct{}

func (c *safeRestyClient) R() *safeRestyRequest { return &safeRestyRequest{} }
func (r *safeRestyRequest) Get(url string) {}
