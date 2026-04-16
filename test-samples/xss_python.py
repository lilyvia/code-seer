from flask import render_template_string
from django.http import HttpResponse

user_input = "<script>alert('xss')</script>"

# Vulnerable: f-string with HTML
def xss_fstring():
    return f"<div>{user_input}</div>"

# Vulnerable: string concatenation in HTML
def xss_concat():
    return "<div>" + user_input + "</div>"

# Vulnerable: Flask render_template_string with user input
def xss_flask():
    return render_template_string("<div>{{ user_input }}</div>")

# Vulnerable: Django HttpResponse with concatenation
def xss_django():
    return HttpResponse("<div>" + user_input + "</div>")

# Vulnerable: Django HttpResponse with f-string
def xss_django_fstring():
    return HttpResponse(f"<div>{user_input}</div>")

# Vulnerable: Markup bypass
def xss_markup():
    from markupsafe import Markup
    return Markup(user_input)
