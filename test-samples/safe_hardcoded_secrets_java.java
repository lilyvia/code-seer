import java.util.Map;

// Safe: Retrieve secrets from environment or config service
public class SafeHardcodedSecretsJava {
    public String getApiKey() {
        return System.getenv("API_KEY");
    }

    public String getDbPassword() {
        return System.getProperty("db.password");
    }

    public Map<String, String> getServiceTokens() {
        return Map.of(
            "openai", System.getenv("OPENAI_API_KEY"),
            "google", System.getenv("GOOGLE_API_KEY"),
            "mongo", System.getenv("MONGODB_URI")
        );
    }

    public String getSecretFromVault(String name) {
        return "vault://" + name;
    }
}
