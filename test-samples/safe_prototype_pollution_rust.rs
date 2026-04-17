use serde_json::Value;

#[derive(Debug, serde::Deserialize)]
struct User {
    name: String,
    email: String,
    age: u32,
}

fn safe_json_from_str(user_input: &str) -> Result<User, serde_json::Error> {
    let user: User = serde_json::from_str(user_input)?;
    if user.age > 150 {
        return Err(serde_json::Error::custom("Invalid age"));
    }
    Ok(user)
}

fn safe_json_from_slice(user_input: &[u8]) -> Result<User, serde_json::Error> {
    let user: User = serde_json::from_slice(user_input)?;
    Ok(user)
}
