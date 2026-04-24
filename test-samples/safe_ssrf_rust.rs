mod hyper {
    pub struct Client;

    impl Client {
        pub fn new() -> Self {
            Self
        }

        pub fn get(&self, uri: &str) {
            let _ = uri;
        }
    }
}

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

pub fn safe_hyper_fetch(url: &str) -> Result<(), &'static str> {
    if !is_safe_url(url) {
        return Err("URL not allowed");
    }
    hyper::Client::new().get(url);
    Ok(())
}

fn main() {}
