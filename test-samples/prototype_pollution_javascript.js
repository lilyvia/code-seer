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

function false_negative_expansion_proto_js(_, req, target) {
    Object.setPrototypeOf(target, req.body);
    _.set(target, req.query.path, req.body.value);
    target = { ...req.body };
    Object.defineProperty(target, req.query.key, { value: req.body.value });
}

function false_negative_additional_proto_js(_, req, target, defaults, userInput, obj) {
    _.mergeWith(target, req.body);
    _.defaultsDeep(defaults, userInput);
    _.unset(obj, '__proto__.toString');
}
