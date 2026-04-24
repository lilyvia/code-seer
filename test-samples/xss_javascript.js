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

function false_negative_expansion_xss_js(element, userInput, $sce, React) {
    element.outerHTML = userInput;
    element.setAttribute("href", userInput);
    $sce.trustAsHtml(userInput);
    React.createElement('div', { dangerouslySetInnerHTML: { __html: userInput } });
}

function false_negative_expansion_additional_xss(element, userInput, $sce, unsafeHTML, React) {
    // Vulnerable: trust bypasses and DOM insertion APIs receive user input.
    $sce.bypassSecurityTrustHtml(userInput);
    $sce.bypassSecurityTrustScript(userInput);
    element.append(userInput);
    element.prepend(userInput);
    unsafeHTML(userInput);
    React.createElement('section', { className: 'profile', dangerouslySetInnerHTML: { __html: userInput } });
}

const svelteTemplate = `{@html userInput}`;
