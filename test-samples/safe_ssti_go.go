package main

import (
	"html/template"
	"os"
)

func safeTemplateParse(data interface{}) error {
	tmpl, _ := template.ParseFiles("safe_template.html")
	return tmpl.Execute(os.Stdout, data)
}

func safeStaticTemplate(data interface{}) error {
	tmpl, _ := template.ParseFiles("hello_template.html")
	return tmpl.Execute(os.Stdout, data)
}
