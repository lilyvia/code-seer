function buildSafeRedirectTarget(userUrl, allowedOrigin) {
    const parsed = new URL(userUrl, allowedOrigin);

    if (parsed.origin !== allowedOrigin) {
        throw new Error('invalid redirect target');
    }

    return `${parsed.pathname}${parsed.search}${parsed.hash}`;
}

function safeOpenRedirect(userUrl, res, reply, ctx, allowedOrigin) {
    const redirectTarget = buildSafeRedirectTarget(userUrl, allowedOrigin);

    res.setHeader('Location', redirectTarget);
    reply.header('Location', redirectTarget);
    ctx.set('Location', redirectTarget);
    window.location.assign('/dashboard');

    return redirectTarget;
}
