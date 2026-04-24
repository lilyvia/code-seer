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
