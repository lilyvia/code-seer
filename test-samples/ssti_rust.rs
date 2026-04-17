use tera::{Tera, Context};
use handlebars::Handlebars;

fn vulnerable_tera_one_off(user_template: &str, context: &Context) -> Result<String, tera::Error> {
    Tera::one_off(user_template, context, false)
}

fn vulnerable_handlebars_render(user_template: &str, data: &serde_json::Value) -> Result<String, handlebars::RenderError> {
    let mut handlebars = Handlebars::new();
    handlebars.render_template(user_template, data)
}
