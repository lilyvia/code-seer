use std::process::Command;

fn safe_cmd_exec() {
    let entries = std::fs::read_dir(".").unwrap();
    for entry in entries {
        println!("{}", entry.unwrap().path().display());
    }
}

fn safe_hardcoded_command() {
    let mut command = Command::new("ls");
    command.arg("-la");
    let _ = command.status();
}

fn main() {}
