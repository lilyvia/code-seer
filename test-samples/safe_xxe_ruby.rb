require 'json'

# Safe: Use JSON instead of XML for untrusted data
class SafeXxe
  def safe_parse(data)
    JSON.parse(data)
  end
end
