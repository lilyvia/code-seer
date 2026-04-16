package main

import (
	"fmt"
	"io"
	"net/http"
)

func vulnerableXSS(w http.ResponseWriter, r *http.Request, userInput string, c *ginContext) {
	fmt.Fprintf(w, "<div>%s</div>", userInput)
	fmt.Fprint(w, "<div>"+userInput+"</div>")
	io.WriteString(w, "<div>"+userInput+"</div>")
	w.Write([]byte("<div>" + userInput + "</div>"))
	c.String(200, "<div>"+userInput+"</div>")
	c.HTML(200, "<div>"+userInput+"</div>")
}

type ginContext struct{}

func (g *ginContext) String(code int, format string, values ...interface{}) {}
func (g *ginContext) HTML(code int, html string)                            {}
