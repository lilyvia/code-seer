using System;
using Microsoft.AspNetCore.Mvc;

public class OpenRedirectController : Controller
{
    public void VulnerableResponseRedirect(string userUrl)
    {
        Response.Redirect(userUrl);
    }

    public IActionResult VulnerableRedirect(string userUrl)
    {
        return Redirect(userUrl);
    }

    public IActionResult VulnerableRedirectPermanent(string userUrl)
    {
        return RedirectPermanent(userUrl);
    }
}
