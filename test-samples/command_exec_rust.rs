use std::process::Command;

mod duct {
    pub fn cmd(program: &str, args: [&str; 1]) {
        let _ = (program, args);
    }
}

fn test_cmd_exec(user_cmd: &str, args: Vec<&str>) {
    let _ = Command::new(user_cmd).output();
    let _ = Command::new(user_cmd).arg("-l").spawn();
    let _ = Command::new(user_cmd).args(&args).status();
    let _ = std::process::Command::new(user_cmd).output();
}

fn false_negative_expansion_rust_command(user_cmd: &str) {
    let _ = Command::new("sh").arg("-c").arg(user_cmd).output();
    let _ = Command::new("sh").arg("-c").arg(user_cmd).spawn();
    duct::cmd(user_cmd, ["--version"]);
}

fn main() {}
