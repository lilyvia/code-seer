package main

import (
	"html/template"
	"os"
)

func vulnerableTemplateParse(userTemplate string, data interface{}) error {
	tmpl, _ := template.New("user").Parse(userTemplate)
	return tmpl.Execute(os.Stdout, data)
}

func vulnerableHtmlTemplateParse(userTemplate string, data interface{}) error {
	tmpl, _ := template.New("user").Parse(userTemplate)
	return tmpl.Execute(os.Stdout, data)
}
