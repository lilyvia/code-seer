function vulnerableAssign(target, req) {
    return Object.assign(target, req.body);
}

function vulnerableMerge(defaults, req, _) {
    return _.merge(defaults, req.body);
}

function vulnerableDynamicKey(target, req) {
    target[req.query.key] = req.body.value;
    return target;
}
