# Safe: Read secrets from environment variables
class SafeSecrets
  def api_key
    ENV['API_KEY']
  end

  def db_password
    ENV.fetch('DB_PASSWORD', nil)
  end

  def secret_from_vault(name)
    "vault://#{name}"
  end
end
