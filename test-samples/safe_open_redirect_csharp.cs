using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;

public class SafeOpenRedirectController : Controller
{
    private static readonly HashSet<string> AllowedPaths = new HashSet<string> { "/home", "/dashboard" };

    public string SafeValidate(string target)
    {
        if (!AllowedPaths.Contains(target))
        {
            return "/";
        }
        return target;
    }

    public void SafeResponseRedirect(string userUrl)
    {
        var safe = SafeValidate(userUrl);
        Response.Redirect(safe);
    }

    public IActionResult SafeHardcodedRedirect()
    {
        return Redirect("/dashboard");
    }

    public IActionResult SafeLocalRedirect(string userUrl)
    {
        return LocalRedirect(userUrl);
    }
}
