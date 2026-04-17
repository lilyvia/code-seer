use serde_json::Value;

fn vulnerable_json_from_str(user_input: &str) -> Result<Value, serde_json::Error> {
    serde_json::from_str::<Value>(user_input)
}

fn vulnerable_json_from_slice(user_input: &[u8]) -> Result<Value, serde_json::Error> {
    serde_json::from_slice::<Value>(user_input)
}

fn vulnerable_bincode_deserialize(user_input: &[u8]) -> Result<Value, bincode::Error> {
    bincode::deserialize::<Value>(user_input)
}
