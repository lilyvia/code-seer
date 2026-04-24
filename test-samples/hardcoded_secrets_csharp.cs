using System;

public class HardcodedSecretsCSharp
{
    public static void Main()
    {
        // Match: string apiKey = "..."
        string apiKey = "sk1234567890abcdef";

        // Match: string password = "..."
        string password = "MySecret123";

        // Match: string dbPassword = "..."
        string dbPassword = "DbPass1234";

        // Match: string connectionString = "Server=..."
        string connectionString = "Server=myServerAddress;Database=myDataBase;User Id=myUsername;Password=myPassword;";

        // Match: string awsKey = "AKIA..."
        string awsKey = "AKIAIOSFODNN7EXAMPLE";

        // Match: string slackToken = "xoxb-..."
        string slackToken = "xoxb-123456789012-abcdefghijklmnop";

        // Match: string privateKey = "-----BEGIN PRIVATE KEY-----"
        string privateKey = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----";

        // Match: string token = "..." (24+ chars)
        string token = "d2hhdGV2ZXI6eW91OnR5cGU6aGVyZQ==";

        string openAiToken = "sk-123456789012345678901234";
        string googleApiKey = "AIza12345678901234567890123456789012345";
        string mongoUri = "mongodb://appuser:apppass@localhost/appdb";
    }
}
