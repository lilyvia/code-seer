use std::path::Path;

// Safe: Validate path without using File::open or fs::read
pub fn safe_path(base_dir: &str, usr_path: &str) -> Result<String, &'static str> {
    let base = Path::new(base_dir).canonicalize().map_err(|_| "bad base")?;
    let dest = base.join(usr_path).canonicalize().map_err(|_| "bad path")?;
    if !dest.starts_with(&base) {
        return Err("path traversal");
    }
    Ok(dest.to_string_lossy().to_string())
}
