using Microsoft.AspNetCore.Mvc;

public class xss_csharp : ControllerBase
{
    public IActionResult VulnerableContent(string userInput)
    {
        Response.Write(userInput);
        Response.Write("<div>" + userInput + "</div>");
        return Content("<div>" + userInput + "</div>");
    }

    public IActionResult VulnerableContentResult(string userInput)
    {
        return new ContentResult { Content = "<div>" + userInput + "</div>" };
    }

    public void FalseNegativeExpansion(dynamic Html, string userContent)
    {
        Html.Raw(userContent);
    }
}
