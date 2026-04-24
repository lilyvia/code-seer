package main

import (
	"bytes"
	"encoding/gob"
	"encoding/json"
	"encoding/xml"
	"io"
)

type mockYAML struct{}
type mockProto struct{}
type mockMsgpack struct{}

func (m mockYAML) Unmarshal(data []byte, out any) error { return nil }
func (m mockProto) Unmarshal(data []byte, out any) error { return nil }
func (m mockMsgpack) Unmarshal(data []byte, out any) error { return nil }

var yaml = mockYAML{}
var proto = mockProto{}
var msgpack = mockMsgpack{}

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

func false_negative_expansion_go_deser(reader io.Reader, userData []byte, out any) error {
	var dynamic map[string]interface{}
	if err := json.Unmarshal(userData, &dynamic); err != nil {
		return err
	}
	if err := gob.NewDecoder(bytes.NewReader(userData)).Decode(&dynamic); err != nil {
		return err
	}
	json.NewDecoder(reader).Decode(&out)
	proto.Unmarshal(userData, &out)
	xml.NewDecoder(reader).Decode(&out)
	msgpack.Unmarshal(userData, &out)
	return nil
}
