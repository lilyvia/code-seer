using System;
using System.Net;

// Safe: Validate URL against allowlist
public class SafeSsrf
{
    private static readonly string[] AllowedHosts = { "api.example.com", "files.example.com" };

    public bool IsSafeUrl(string url)
    {
        if (Uri.TryCreate(url, UriKind.Absolute, out var uri))
        {
            return uri.Scheme == Uri.UriSchemeHttps && Array.Exists(AllowedHosts, h => h == uri.Host);
        }
        return false;
    }

    public string SafeWebClientFetch(string url)
    {
        if (!IsSafeUrl(url))
        {
            throw new ArgumentException("URL not allowed", nameof(url));
        }
        using (var webClient = new WebClient())
        {
            return webClient.DownloadString(url);
        }
    }
}
