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

class FalseNegativeExpansionSstiJava {
    void false_negative_expansion(Jinjava jinjava, Handlebars handlebars, VelocityEngine velocity, String userTemplate) {
        jinjava.render(userTemplate, model);
        handlebars.compileInline(userTemplate);
        velocity.evaluate(context, writer, "log", userTemplate);
    }

    void false_negative_additional(VelocityEngine velocity, Configuration cfg, Object ctx, Object writer, Object log, String userTemplate) throws Exception {
        velocity.evaluate(ctx, writer, log, userTemplate);
        Template template = new Template("user", userTemplate, cfg);
    }
}
