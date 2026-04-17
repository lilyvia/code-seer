// Safe: Use manual parsing or JSON with strict schema validation
// Avoid serde_json::from_str, bincode::deserialize for untrusted data

fn safe_parse_json(data: &str) -> Result<&str, &'static str> {
    if data.len() > 1024 {
        return Err("Payload too large");
    }
    // In production, validate against a strict schema
    Ok(data)
}
