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

    public string GetOpenAiToken()
    {
        return Environment.GetEnvironmentVariable("OPENAI_API_KEY");
    }

    public string GetGoogleApiKey()
    {
        return Environment.GetEnvironmentVariable("GOOGLE_API_KEY");
    }

    public string GetMongoUri()
    {
        return Environment.GetEnvironmentVariable("MONGODB_URI");
    }
}
