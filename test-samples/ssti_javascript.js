const ejs = require('ejs');
const Handlebars = require('handlebars');
const Mustache = require('mustache');
const pug = require('pug');
const _ = require('lodash');

function vulnerableEjsCompile(userTemplate, data) {
    const template = ejs.compile(userTemplate);
    return template(data);
}

function vulnerableEjsRender(userTemplate, data) {
    return ejs.render(userTemplate, data);
}

function vulnerableHandlebarsCompile(userTemplate, data) {
    const template = Handlebars.compile(userTemplate);
    return template(data);
}

function vulnerableMustacheRender(userTemplate, data) {
    return Mustache.render(userTemplate, data);
}

function vulnerablePugCompile(userTemplate, data) {
    const template = pug.compile(userTemplate);
    return template(data);
}

function vulnerablePugRender(userTemplate, data) {
    return pug.render(userTemplate, data);
}

function vulnerableLodashTemplate(userTemplate, data) {
    const template = _.template(userTemplate);
    return template(data);
}
