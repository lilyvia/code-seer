package main

import (
	"encoding/xml"
	"strings"
)

type XMLEntity struct {
	Name string `xml:"name"`
}

func vulnerableXXE(xmlInput string) error {
	var u XMLEntity
	return xml.Unmarshal([]byte(xmlInput), &u)
}

func vulnerableXXEDecoder(xmlInput string) error {
	var u XMLEntity
	decoder := xml.NewDecoder(strings.NewReader(xmlInput))
	return decoder.Decode(&u)
}
