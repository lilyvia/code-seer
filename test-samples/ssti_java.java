import freemarker.template.Configuration;
import freemarker.template.Template;
import org.springframework.ui.freemarker.FreeMarkerTemplateUtils;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

import java.io.StringWriter;

class SstiJava {
    public String vulnerableFreemarker(String userTemplate, Object model) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        Template template = new Template("user", userTemplate, cfg);
        return FreeMarkerTemplateUtils.processTemplateIntoString(template, model);
    }

    public String vulnerableThymeleaf(String userTemplate, Object data) {
        TemplateEngine engine = new TemplateEngine();
        Context ctx = new Context();
        ctx.setVariable("data", data);
        return engine.process(userTemplate, ctx);
    }

    public String vulnerableTemplateProcess(String userTemplate, Object model) throws Exception {
        Configuration cfg = new Configuration(Configuration.VERSION_2_3_31);
        Template template = new Template("user", userTemplate, cfg);
        StringWriter out = new StringWriter();
        template.process(model, out);
        return out.toString();
    }
}
