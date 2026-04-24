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

function safeLocationAssignment(allowedPaths, userPath) {
    if (!allowedPaths.includes(userPath)) {
        throw new Error('invalid path');
    }
    location.href = userPath;
    window.location.href = userPath;
}

function safeRedirectWithValidatedPath(userPath) {
    const allowedPaths = ['/home', '/dashboard'];
    if (!allowedPaths.includes(userPath)) {
        throw new Error('invalid path');
    }
    return NextResponse.redirect(userPath);
}
