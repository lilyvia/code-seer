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

func false_negative_expansion_go_command(ctx context.Context, userCmd string) {
    exec.CommandContext(ctx, userCmd).Run()
    os.StartProcess(userCmd, []string{userCmd}, nil)
    syscall.Exec(userCmd, []string{userCmd}, nil)
}
