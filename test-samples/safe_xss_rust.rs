use actix_web::{HttpResponse, web::Html};

fn safe_xss(name: &str) -> String {
    // Return plain text, no HTML
    name.to_string()
}
