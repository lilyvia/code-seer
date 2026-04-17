use actix_web::{HttpResponse, HttpRequest};
use warp::redirect;

fn vulnerable_actix_redirect(user_url: &str) -> HttpResponse {
    HttpResponse::Found().header("Location", user_url)
}

fn vulnerable_rocket_redirect(user_url: &str) {
    redirect::to(user_url);
}

fn vulnerable_warp_redirect(user_url: &str) {
    warp::redirect::see_other(user_url.parse().unwrap());
}

fn vulnerable_axum_redirect(user_url: &str) {
    Redirect::to(user_url);
}
