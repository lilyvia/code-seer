import java.net.URI;
import java.net.URL;
import java.net.URLConnection;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

class SsrfJava {
    public void vulnerable(String userUrl) throws Exception {
        URLConnection conn = new URL(userUrl).openConnection();
        conn.connect();

        HttpRequest req = HttpRequest.newBuilder(URI.create(userUrl)).build();
        HttpClient.newHttpClient().send(req, HttpResponse.BodyHandlers.ofString());

        new URL("http://169.254.169.254/latest/meta-data/").openConnection();
    }
}

class FalseNegativeExpansionSsrfJava {
    void false_negative_expansion(String userUrl, RestTemplate rest, WebClient webClient) throws Exception {
        new URL(userUrl).openStream();
        rest.getForObject(userUrl, String.class);
        webClient.get().uri(userUrl);
    }

    void false_negative_expansion_http_clients(String userUrl, CloseableHttpClient httpClient) throws Exception {
        ClassicHttpRequest userRequest = new ClassicHttpRequest(userUrl);
        HttpClients.createDefault().execute(userRequest);
        httpClient.execute(userRequest);
        URL userInputUrl = new URL(userUrl);
        userInputUrl.openConnection();
    }
}

class RestTemplate { Object getForObject(String url, Class<?> type) { return null; } }
class WebClient { WebClient get() { return this; } WebClient uri(String uri) { return this; } }
class ClassicHttpRequest { ClassicHttpRequest(String url) {} }
class HttpClients { static CloseableHttpClient createDefault() { return new CloseableHttpClient(); } }
class CloseableHttpClient { Object execute(ClassicHttpRequest request) { return null; } }
