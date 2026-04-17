from markupsafe import escape


# Safe: Escape user input before HTML output
def safe_html(user_input):
    escaped = escape(user_input)
    return f"<div>{escaped}</div>"


# Safe: Use template engine auto-escaping
def safe_render(user_name):
    return render_template("profile.html", name=user_name)


# Safe: Return plain text instead of raw HTML
def safe_text(user_input):
    return {"message": user_input}
