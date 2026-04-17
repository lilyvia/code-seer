using System;

class SafeSstiCsharp {
    public string SafeTemplateRender(object data) {
        var template = GetTemplateFromFile("safe_template.liquid");
        return template.Render(data);
    }

    public string SafeStaticTemplate(object data) {
        var template = GetTemplateFromString("Hello {{ name }}!");
        return template.Render(data);
    }

    private dynamic GetTemplateFromFile(string path) {
        return null;
    }

    private dynamic GetTemplateFromString(string content) {
        return null;
    }
}
