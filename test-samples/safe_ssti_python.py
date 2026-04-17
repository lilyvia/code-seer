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


def render_template(template_name, **context):
    return template_name, context


SAFE_TEMPLATE = "Hello {{ user }}"


def render_static_template(context):
    html1 = render_template("profile.html", user=context["user"])
    html2 = Template(SAFE_TEMPLATE).render(context)
    html3 = Environment().from_string(SAFE_TEMPLATE).render(context)
    return html1, html2, html3
