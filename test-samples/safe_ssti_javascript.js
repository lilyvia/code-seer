const ejs = require('ejs');
const Handlebars = require('handlebars');

function safeEjsRenderFile(data) {
    return ejs.renderFile('safe_template.ejs', data);
}

function safeStaticEjs(data) {
    return ejs.render('Hello <%= name %>!', data);
}

function safeHandlebarsCompile(data) {
    const template = Handlebars.compile('Hello {{name}}!');
    return template(data);
}
