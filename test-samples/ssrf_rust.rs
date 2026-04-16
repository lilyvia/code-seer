use reqwest;
use ureq;

async fn test_ssrf(user_url: &str) {
    let _ = reqwest::get(user_url).await;
    let _ = ureq::get(user_url).call();
    let client = reqwest::Client::new();
    let _ = client.get(user_url).send().await;
    let _ = surf::get(user_url).await;
    let _ = isahc::get(user_url);
    let _ = isahc::get_async(user_url).await;
}
