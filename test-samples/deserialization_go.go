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

func false_negative_expansion_go_deser(reader io.Reader, userData []byte, out any) {
    json.NewDecoder(reader).Decode(&out)
    proto.Unmarshal(userData, &out)
    xml.NewDecoder(reader).Decode(&out)
    msgpack.Unmarshal(userData, &out)
}
