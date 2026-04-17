// Safe Rust patterns that avoid command execution

fn safe_cmd_exec() {
    // Use stdlib functions instead of external commands
    let entries = std::fs::read_dir(".").unwrap();
    for entry in entries {
        println!("{}", entry.unwrap().path().display());
    }
}
