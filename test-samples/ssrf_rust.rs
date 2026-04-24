mod reqwest {
    pub fn get(url: &str) {
        let _ = url;
    }

    pub struct Client;

    impl Client {
        pub fn new() -> Self {
            Self
        }

        pub fn get(&self, url: &str) -> Request {
            let _ = url;
            Request
        }
    }

    pub struct Request;

    impl Request {
        pub fn send(self) {}
    }
}

mod ureq {
    pub struct Request;

    pub fn get(url: &str) -> Request {
        let _ = url;
        Request
    }

    impl Request {
        pub fn call(self) {}
    }
}

mod surf {
    pub fn get(url: &str) {
        let _ = url;
    }
}

mod isahc {
    pub fn get(url: &str) {
        let _ = url;
    }

    pub fn get_async(url: &str) {
        let _ = url;
    }
}

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

fn test_ssrf(user_url: &str) {
    reqwest::get(user_url);
    ureq::get(user_url).call();
    let client = reqwest::Client::new();
    client.get(user_url).send();
    surf::get(user_url);
    isahc::get(user_url);
    isahc::get_async(user_url);
}

fn false_negative_expansion_hyper(user_uri: &str) {
    hyper::Client::new().get(user_uri);
}

fn main() {}
