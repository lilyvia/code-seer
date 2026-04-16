require 'erb'

user_input = params[:input]

render inline: "<div>#{user_input}</div>"
render html: raw(user_input)
render html: user_input.html_safe
ERB.new(user_input).result
ERB.new(user_input).result(binding)
response.write(user_input)
content_tag(:div, raw(user_input))
raw(user_input)
