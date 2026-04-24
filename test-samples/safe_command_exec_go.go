package main

import "os/exec"

// Safe: Use hardcoded command with argument list
func safeLs() ([]byte, error) {
	cmd := exec.Command("ls", "-la")
	return cmd.Output()
}

func safeStartFixedCommand() error {
	cmd := exec.Command("date")
	return cmd.Start()
}

// Safe: Whitelist allowed commands
var allowedCommands = map[string]bool{"date": true, "whoami": true, "pwd": true}

func safeRun(cmd string) ([]byte, error) {
	if !allowedCommands[cmd] {
		return nil, exec.ErrNotFound
	}
	c := exec.Command(cmd)
	return c.Output()
}
