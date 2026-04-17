use actix_web::HttpResponse;

fn safe_validate(target: &str) -> Result<&str, &str> {
    let allowed = ["/home", "/dashboard"];
    if allowed.contains(&target) {
        Ok(target)
    } else {
        Err("非法跳转目标")
    }
}

fn safe_actix_redirect(user_url: &str) -> HttpResponse {
    match safe_validate(user_url) {
        Ok(safe) => HttpResponse::Found().header("Location", safe),
        Err(_) => HttpResponse::Forbidden().finish(),
    }
}

fn safe_hardcoded_redirect() -> HttpResponse {
    HttpResponse::Found().header("Location", "/dashboard")
}

fn safe_rocket_redirect() {
    redirect::to("/dashboard");
}
