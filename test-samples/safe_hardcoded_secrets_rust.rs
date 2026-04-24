use std::env;

// Safe: Read secrets from environment variables
pub fn get_api_key() -> Result<String, env::VarError> {
    env::var("API_KEY")
}

pub fn get_db_password() -> Result<String, env::VarError> {
    env::var("DB_PASSWORD")
}

pub fn get_service_tokens() -> Result<(String, String, String), env::VarError> {
    Ok((
        env::var("OPENAI_API_KEY")?,
        env::var("GOOGLE_API_KEY")?,
        env::var("MONGODB_URI")?,
    ))
}
