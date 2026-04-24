use actix_web::{HttpResponse, web::Html};

mod actix_web {
    pub struct HttpResponse;

    impl HttpResponse {
        pub fn Ok() -> Self {
            Self
        }

        pub fn body(self, body: String) -> Self {
            let _ = body;
            self
        }
    }

    pub mod web {
        pub struct Html(pub String);
    }
}

mod maud {
    pub struct PreEscaped<'a>(pub &'a str);
}

mod askama {
    pub struct Html<'a>(pub &'a str);
}

fn test_xss(name: &str) {
    // XSS patterns
    let html = format!("<div>{}</div>", name);
    let response = HttpResponse::Ok().body(format!("<h1>{}</h1>", name));
    let html2 = Html(format!("<script>alert('{}')</script>", name));
    let html3 = maud::PreEscaped(name);
    let html4 = askama::Html(name);
}
