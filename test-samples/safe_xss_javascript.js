function safeXSS(userInput, trustedOrigin) {
    const div = document.createElement('div');
    const ref = { current: document.createElement('div') };

    div.textContent = userInput;
    ref.current.textContent = userInput;
    window.postMessage({ type: 'preview', value: userInput }, trustedOrigin);
}
