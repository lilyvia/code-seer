use actix_web::{HttpResponse, web::Html};

fn test_xss(name: &str) {
    // XSS patterns
    let html = format!("<div>{}</div>", name);
    let response = HttpResponse::Ok().body(format!("<h1>{}</h1>", name));
    let html2 = Html(format!("<script>alert('{}')</script>", name));
}
