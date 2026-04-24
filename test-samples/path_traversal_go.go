package main

import (
	"os"
	"path/filepath"
)

func readFile(userPath string) {
	os.Open(userPath)
	os.ReadFile(userPath)
}

func writeFile(uploadPath string, content []byte) {
	os.Create(uploadPath)
	os.WriteFile(uploadPath, content, 0644)
}

func deleteFile(userPath string) {
	os.Remove(userPath)
}

func joinPath(baseDir, userPath string) string {
	return filepath.Join(baseDir, userPath)
}

func parentPath(userPath string) {
	os.Open("../" + userPath)
	os.Remove("../" + userPath)
}

func parentJoin(baseDir, userPath string) string {
	return filepath.Join(baseDir, "../"+userPath)
}

func false_negative_expansion_path_go(userPath string) {
    os.Rename(userPath, "/tmp/out")
    os.ReadDir(userPath)
    os.MkdirAll(userPath, 0755)
    os.Stat(userPath)
    filepath.Walk(userPath, nil)
}
