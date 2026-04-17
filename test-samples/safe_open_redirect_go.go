package main

import (
	"fmt"
	"net/http"
	"net/url"
)

func safeRedirect(target string) (string, error) {
	allowedHosts := map[string]bool{"example.com": true}
	u, err := url.Parse(target)
	if err != nil {
		return "", err
	}
	if u.Host != "" && !allowedHosts[u.Host] {
		return "", fmt.Errorf("非法跳转目标")
	}
	return target, nil
}

func safeOpenRedirect(w http.ResponseWriter, r *http.Request, userUrl string) {
	safe, _ := safeRedirect(userUrl)
	http.Redirect(w, r, safe, http.StatusFound)
}

func safeHardcodedRedirect(w http.ResponseWriter, r *http.Request) {
	http.Redirect(w, r, "/dashboard", http.StatusFound)
}

func safeCtxRedirect(ctx interface{}) {
	ctx.Redirect(302, "/home")
}
