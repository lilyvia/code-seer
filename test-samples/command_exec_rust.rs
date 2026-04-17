use std::process::Command;

fn test_cmd_exec(user_cmd: &str, args: Vec<&str>) {
    // Command execution patterns
    let _ = Command::new(user_cmd).output();
    let _ = Command::new(&user_cmd).arg("-l").spawn();
    let _ = Command::new(&user_cmd).args(&args).status();
    let _ = std::process::Command::new(user_cmd).output();
}
