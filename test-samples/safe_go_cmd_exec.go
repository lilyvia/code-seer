package main

import "os/exec"

// Safe: Use hardcoded command with argument list
func safeLs() ([]byte, error) {
	return exec.Command("ls", "-la").Output()
}

// Safe: Whitelist allowed commands
var allowedCommands = map[string]bool{"date": true, "whoami": true, "pwd": true}

func safeRun(cmd string) ([]byte, error) {
	if !allowedCommands[cmd] {
		return nil, exec.ErrNotFound
	}
	return exec.Command(cmd).Output()
}
