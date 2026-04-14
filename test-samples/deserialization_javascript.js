function vulnerableDeserialization(userInput) {
    const obj = eval(userInput);
    const fn = new Function(userInput);
    return obj;
}
