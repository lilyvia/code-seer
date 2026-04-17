package main

import (
	"fmt"
	"path/filepath"
	"strings"
)

// Safe: Validate user path without filepath.Join
func safePath(baseDir, userPath string) (string, error) {
	baseAbs, err := filepath.Abs(baseDir)
	if err != nil {
		return "", err
	}
	target := filepath.Clean(baseAbs + "/" + userPath)
	sep := string(filepath.Separator)
	if !strings.HasPrefix(target+sep, baseAbs+sep) {
		return "", fmt.Errorf("path traversal detected")
	}
	return target, nil
}
