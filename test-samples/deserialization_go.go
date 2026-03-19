package main

import (
	"bytes"
	"encoding/gob"
)

type mockYAML struct{}

func (m mockYAML) Unmarshal(data []byte, out any) error {
	return nil
}

var yaml = mockYAML{}

func parseGobAndYaml(input []byte) error {
	var req map[string]any

	decoder := gob.NewDecoder(bytes.NewReader(input))
	if err := decoder.Decode(&req); err != nil {
		return err
	}

	if err := yaml.Unmarshal(input, &req); err != nil {
		return err
	}

	return nil
}
