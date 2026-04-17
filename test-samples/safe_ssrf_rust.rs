// Safe: Validate URL before fetching
pub fn is_safe_url(url: &str) -> bool {
    url.starts_with("https://api.example.com/")
        || url.starts_with("https://files.example.com/")
}

pub fn safe_fetch(url: &str) -> Result<String, &'static str> {
    if !is_safe_url(url) {
        return Err("URL not allowed");
    }
    Ok(format!("fetching {}", url))
}
