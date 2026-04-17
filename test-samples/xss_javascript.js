function vulnerableXSS(userInput) {
    const div = document.createElement('div');
    const ref = { current: document.createElement('div') };
    div.innerHTML = userInput;
    ref.current.innerHTML = userInput;
    document.write(userInput);
    window.postMessage(userInput, '*');
    eval(userInput);
    setTimeout(userInput, 1000);
    new Function(userInput);
}
