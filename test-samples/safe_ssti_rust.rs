use tera::{Tera, Context};
use handlebars::Handlebars;

fn safe_tera_render(context: &Context) -> Result<String, tera::Error> {
    let tera = Tera::new("templates/**/*")?;
    tera.render("safe_template.html", context)
}

fn safe_handlebars_render(data: &serde_json::Value) -> Result<String, handlebars::RenderError> {
    let mut handlebars = Handlebars::new();
    handlebars.register_template_string("safe", "Hello {{name}}!")?;
    handlebars.render("safe", data)
}
