package main

import (
	"net/http"
)

func vulnerableOpenRedirect(w http.ResponseWriter, r *http.Request, userUrl string) {
	http.Redirect(w, r, userUrl, http.StatusFound)
}

func vulnerableCtxRedirect(ctx interface{}, userUrl string) {
	ctx.Redirect(302, userUrl)
}

func vulnerableCRedirect(c interface{}, userUrl string) {
	c.Redirect(userUrl, 302)
}
