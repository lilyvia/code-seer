require 'json'

# Safe: Use JSON.parse instead of Marshal.load
class SafeDeserialization
  def safe_parse(data)
    JSON.parse(data)
  end

  def safe_parse_without_additions(data)
    JSON.parse(data)
  end

  def safe_parse_with_schema(data)
    obj = JSON.parse(data)
    raise 'Invalid schema' unless obj.is_a?(Hash) && obj.key?('name')
    obj
  end
end
