require 'uri'

# Safe: Validate URL against allowlist
class SafeSsrf
  ALLOWED_HOSTS = %w[api.example.com files.example.com].freeze

  def safe?(url)
    uri = URI.parse(url)
    uri.scheme == 'https' && ALLOWED_HOSTS.include?(uri.host)
  rescue URI::InvalidURIError
    false
  end

  def fetch(url)
    raise 'URL not allowed' unless safe?(url)
    "fetching #{url}"
  end
end
