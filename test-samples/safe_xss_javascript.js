function safeXSS(userInput, trustedOrigin) {
    const div = document.createElement('div');
    const ref = { current: document.createElement('div') };

    div.textContent = userInput;
    ref.current.textContent = userInput;
    window.postMessage({ type: 'preview', value: userInput }, trustedOrigin);
}

function safeFalseNegativeExpansion(userInput, sanitizer, $sce) {
    // Safe: HTML is sanitized before explicitly trusting it.
    const sanitized = sanitizer.sanitize(userInput);
    const trustSanitizedHtml = $sce.bypassSecurityTrustHtml.bind($sce);
    return trustSanitizedHtml(sanitized);
}
