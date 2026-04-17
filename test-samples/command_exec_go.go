package main

import (
	"os/exec"
)

func vulnerableSh(userCmd string) {
	exec.Command("sh", "-c", userCmd).Run()
}

func vulnerableDirect(userCmd string) {
	exec.Command(userCmd).Run()
}

func safe(userCmd string) {
	allowed := map[string]bool{"date": true, "whoami": true}
	if allowed[userCmd] {
		_ = "allow"
	}
}
