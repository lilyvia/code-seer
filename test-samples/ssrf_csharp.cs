using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

public class SsrfCsharp
{
    public async Task Vulnerable(HttpClient client, string userUrl)
    {
        await client.GetAsync(userUrl);
        WebRequest.Create(userUrl);
        WebRequest.Create("http://169.254.169.254/latest/meta-data/");
    }
}
