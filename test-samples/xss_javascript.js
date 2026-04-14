function vulnerableXSS(userInput) {
    const div = document.createElement('div');
    div.innerHTML = userInput;
    document.write(userInput);
}
