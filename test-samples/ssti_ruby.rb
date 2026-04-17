require 'erb'
require 'haml'
require 'slim'
require 'tilt'

class SstiRuby
  def vulnerable_erb(user_template, context)
    template = ERB.new(user_template)
    template.result(binding)
  end

  def vulnerable_erb_with_hash(user_template, context)
    template = ERB.new(user_template)
    template.result_with_hash(context)
  end

  def vulnerable_haml(user_template, context)
    engine = Haml::Engine.new(user_template)
    engine.render(context)
  end

  def vulnerable_slim(user_template, context)
    Slim::Template.new(user_template).render(context)
  end

  def vulnerable_tilt(user_template, context)
    Tilt.new(user_template).render(context)
  end
end
