# Safe: Escape HTML output
class SafeXss
  def safe_output(usr_input)
    escaped = Rack::Utils.escape_html(usr_input)
    "<div>#{escaped}</div>"
  end

  def safe_text(usr_input)
    usr_input
  end
end
