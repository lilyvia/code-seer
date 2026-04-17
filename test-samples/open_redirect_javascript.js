function vulnerableOpenRedirect(userUrl, res, reply, ctx) {
    res.redirect(userUrl);
    reply.redirect(userUrl);
    ctx.redirect(userUrl);
    location.href = userUrl;
    window.location.href = userUrl;
}
