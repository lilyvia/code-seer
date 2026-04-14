public class HardcodedSecretsJava {
    public static void main(String[] args) {
        // Match: String apiKey = "..."
        String apiKey = "sk1234567890abcdef";

        // Match: String password = "..."
        String password = "MySecret123";

        // Match: String dbPassword = "..."
        String dbPassword = "DbPass1234";

        // Match: String jdbcUrl = "jdbc:mysql://..."
        String jdbcUrl = "jdbc:mysql://localhost:3306/mydb?user=root&password=secret";

        // Match: String awsKey = "AKIA..."
        String awsKey = "AKIAIOSFODNN7EXAMPLE";

        // Match: String slackToken = "xoxb-..."
        String slackToken = "xoxb-123456789012-abcdefghijklmnop";

        // Match: String privateKey = "-----BEGIN RSA PRIVATE KEY-----"
        String privateKey = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----";

        // Match: String secretToken = "..."
        String secretToken = "d2hhdGV2ZXI6eW91OnR5cGU6aGVyZQ==";
    }
}
