function vulnerableXXE(xmlString) {
    const libxmljs = require('libxmljs');
    const doc = libxmljs.parseXml(xmlString);
    return doc;
}
