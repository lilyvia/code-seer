function safeCopySelectedFields(target, req) {
    return Object.assign(target, {
        name: String(req.body.name || ''),
        theme: String(req.body.theme || 'light')
    });
}

function safeAllowlistedAssignment(target, req) {
    const allowedKeys = new Set(['name', 'theme']);
    const key = req.query.key;
    if (!allowedKeys.has(key)) {
        throw new Error('invalid key');
    }

    target.profile = target.profile || {};
    target.profile[key] = String(req.body.value);
    return target;
}

function safeMergeKnownShape(defaults, req, _) {
    return _.merge(defaults, {
        profile: {
            theme: String(req.body.theme || 'light')
        }
    });
}
