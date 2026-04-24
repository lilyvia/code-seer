import freemarker.template.Configuration;
import freemarker.template.Template;

import java.io.StringWriter;

class SafeSstiJava {
    public String safeFreemarker(Object model) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        Template template = cfg.getTemplate("safe_template.ftl");
        StringWriter out = new StringWriter();
        template.process(model, out);
        return out.toString();
    }

    public String safeStaticTemplate(Object model) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        Template template = cfg.getTemplate("safe_template.ftl");
        StringWriter out = new StringWriter();
        template.process(model, out);
        return out.toString();
    }

    public Template safeTemplateFromFile() throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        return cfg.getTemplate("reports/summary.ftl");
    }
}
