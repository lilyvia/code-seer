class Template:
    def __init__(self, source):
        self.source = source

    def render(self, context):
        return self.source, context


class _CompiledTemplate:
    def __init__(self, source):
        self.source = source

    def render(self, context):
        return self.source, context


class Environment:
    def from_string(self, source):
        return _CompiledTemplate(source)


def render_template_string(source, **context):
    return source, context


def render_user_template(user_template, context):
    html1 = render_template_string(user_template, user=context)
    html2 = Template(user_template).render(context)
    html3 = Environment().from_string(user_template).render(context)
    return html1, html2, html3

def false_negative_expansion_ssti_python(user_template):
    mako.template.Template(user_template).render()
    django.template.Template(user_template).render(Context({}))
    jinja2.Environment().from_string(user_template)
