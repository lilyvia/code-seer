package main

import (
	"net/http"
	"strings"
)

func vulnerableSSRF(userURL string) {
	http.Get(userURL)
	http.Post(userURL, "application/json", strings.NewReader("{}"))
	http.Get("http://169.254.169.254/latest/meta-data/")
	var client []byte
	fasthttp.Get(client, userURL)
	resp := &fastResponse{}
	req := &fastRequest{url: userURL}
	fasthttp.Do(req, resp)
	resty.New().R().Get(userURL)
}

var fasthttp fastHTTPClient
var resty restyFactory

type fastHTTPClient struct{}
type fastRequest struct{ url string }
type fastResponse struct{}
type restyFactory struct{}
type restyClient struct{}
type restyRequest struct{}

func (fastHTTPClient) Get(client []byte, url string) {}
func (fastHTTPClient) Do(req *fastRequest, resp *fastResponse) {}
func (restyFactory) New() *restyClient { return &restyClient{} }
func (c *restyClient) R() *restyRequest { return &restyRequest{} }
func (r *restyRequest) Get(url string) {}
func (r *restyRequest) Post(url string) {}
