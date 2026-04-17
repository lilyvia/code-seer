require 'erb'

class SafeSstiRuby
  def safe_erb(context)
    template = ERB.new(File.read('safe_template.erb'))
    template.result_with_hash(user: context[:user])
  end

  def safe_static_erb(context)
    template = ERB.new('Hello <%= user %>!')
    template.result_with_hash(user: context[:user])
  end
end
