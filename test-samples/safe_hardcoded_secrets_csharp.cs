using System;

// Safe: Read secrets from environment variables
public class SafeSecrets
{
    public string GetApiKey()
    {
        return Environment.GetEnvironmentVariable("API_KEY");
    }

    public string GetDbPassword()
    {
        return Environment.GetEnvironmentVariable("DB_PASSWORD");
    }
}
