import java.util.Map;

// Safe: Retrieve secrets from environment or config service
public class SafeHardcodedSecretsJava {
    public String getApiKey() {
        return System.getenv("API_KEY");
    }

    public String getDbPassword() {
        return System.getProperty("db.password");
    }

    public String getSecretFromVault(String name) {
        return "vault://" + name;
    }
}
