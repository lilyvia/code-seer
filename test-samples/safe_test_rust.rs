use std::env;

// Safe Rust patterns that avoid triggering any vulnerability rules

fn safe_auth_check(order_uid: i32, current_uid: i32) -> bool {
    order_uid == current_uid
}

fn safe_cmd() {
    // Use Rust stdlib instead of Command
    let _now = std::time::SystemTime::now();
}

fn safe_xss(usr_input: &str) -> String {
    // Return plain text, no HTML
    usr_input.to_string()
}

fn safe_path(base: &str, usr_path: &str) -> Result<String, &'static str> {
    let base_abs = std::fs::canonicalize(base).map_err(|_| "bad base")?;
    let dest = base_abs.join(usr_path);
    let dest = std::fs::canonicalize(&dest).map_err(|_| "bad path")?;
    if !dest.starts_with(&base_abs) {
        return Err("path traversal");
    }
    Ok(dest.to_string_lossy().to_string())
}

fn safe_ssrf_check(url: &str) -> bool {
    url.starts_with("https://api.example.com/")
}

fn safe_deser() {
    // Use manual parsing instead of serde for untrusted data
}

fn safe_secrets() -> String {
    env::var("API_KEY").unwrap_or_default()
}

fn safe_xxe() {
    // Avoid XML parsers; use JSON or manual validation
}
