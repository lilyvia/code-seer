function vulnerableDeserialization(userInput) {
    const obj = eval(userInput);
    const fn = new Function(userInput);
    return obj;
}

function false_negative_expansion_js_deser(vm, v8, bson, msgpack, userData) {
    vm.runInNewContext(userData, {});
    vm.runInThisContext(userData);
    v8.deserialize(userData);
    bson.deserialize(userData);
    msgpack.decode(userData);
}
