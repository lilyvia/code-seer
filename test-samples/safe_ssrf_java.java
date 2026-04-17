import java.net.URI;
import java.util.Arrays;
import java.util.List;

// Safe: Validate URLs against allowlist before fetching
public class SafeSsrfJava {
    private static final List<String> ALLOWED_HOSTS = Arrays.asList("api.example.com", "files.example.com");

    public boolean isSafeUrl(String url) {
        try {
            URI uri = URI.create(url);
            return "https".equalsIgnoreCase(uri.getScheme()) && ALLOWED_HOSTS.contains(uri.getHost());
        } catch (Exception e) {
            return false;
        }
    }

    public String fetchData(String url) {
        if (!isSafeUrl(url)) {
            throw new IllegalArgumentException("URL not allowed");
        }
        return "fetched: " + url;
    }
}
