function vulnerableOpenRedirect(userUrl, res, reply, ctx) {
    res.redirect(userUrl);
    reply.redirect(userUrl);
    ctx.redirect(userUrl);
    location.href = userUrl;
    window.location.href = userUrl;
    location.replace(userUrl);
    window.location.replace(userUrl);
}

function false_negative_expansion_redirect_js(res, ctx, userUrl) {
    window.location = userUrl;
    window.location.assign(userUrl);
    res.setHeader("Location", userUrl);
    ctx.redirect(userUrl);
}
