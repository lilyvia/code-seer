fn test_deserialization(user_data: &str, bytes: &[u8]) {
    let obj1: User = serde_json::from_str(user_data).unwrap();
    let obj2: User = serde_json::from_slice(bytes).unwrap();
    let obj3: User = bincode::deserialize(bytes).unwrap();
    let obj4: User = postcard::from_bytes(bytes).unwrap();
    let obj5: User = rmp_serde::from_slice(bytes).unwrap();
    let obj6: Config = serde_yaml::from_str(user_data).unwrap();
    let obj7: Config = toml::from_str(user_data).unwrap();
}

fn safe_deserialization(user_data: &str) {
    let obj: User = serde_json::from_str(user_data).unwrap();
}
