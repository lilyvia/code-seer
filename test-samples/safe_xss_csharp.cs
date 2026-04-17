using System;
using System.Net;
using System.Web;

// Safe: Encode HTML output
public class SafeXss
{
    public string SafeOutput(string userInput)
    {
        var encoded = WebUtility.HtmlEncode(userInput);
        return "<div>" + encoded + "</div>";
    }

    public string SafeAttribute(string userInput)
    {
        return HttpUtility.HtmlAttributeEncode(userInput);
    }
}
