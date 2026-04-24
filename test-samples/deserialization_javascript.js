function vulnerableDeserialization(userInput) {
    const obj = eval(userInput);
    const fn = new Function(userInput);
    return obj;
}

function serialize(value) {
    return String(value);
}

const funcster = {
    evaluate(value) {
        return value;
    }
};

function false_negative_expansion_js_deser(vm, v8, bson, msgpack, userData) {
    vm.runInNewContext(userData, {});
    vm.runInThisContext(userData);
    v8.deserialize(userData);
    bson.deserialize(userData);
    msgpack.decode(userData);
    JSON.parse(userData, function revive(key, value) {
        return key === 'code' ? eval(value) : value;
    });
    const serialized = serialize(userData);
    eval(serialized);
    eval(serialize(userData));
    require("javascript-serializer").deserialize(userData);
    funcster.evaluate(userData);
}
