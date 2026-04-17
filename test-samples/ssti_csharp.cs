using DotLiquid;
using Scriban;
using System.IO;

class SstiCsharp {
    public string VulnerableDotLiquid(string userTemplate, object data) {
        var template = Template.Parse(userTemplate);
        return template.Render(Hash.FromAnonymousObject(data));
    }

    public string VulnerableScriban(string userTemplate, object data) {
        var template = Scriban.Template.Parse(userTemplate);
        return template.Render(data);
    }
}
