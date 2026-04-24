struct User;
struct Config;

mod serde_json {
    pub fn from_str<T>(_data: &str) -> Result<T, ()> { Err(()) }
    pub fn from_slice<T>(_data: &[u8]) -> Result<T, ()> { Err(()) }
    pub fn from_reader<T, R: std::io::Read>(_reader: R) -> Result<T, ()> { Err(()) }
}
mod bincode {
    pub fn deserialize<T>(_data: &[u8]) -> Result<T, ()> { Err(()) }
}
mod postcard {
    pub fn from_bytes<T>(_data: &[u8]) -> Result<T, ()> { Err(()) }
}
mod rmp_serde {
    pub fn from_slice<T>(_data: &[u8]) -> Result<T, ()> { Err(()) }
    pub fn from_read<T, R: std::io::Read>(_reader: R) -> Result<T, ()> { Err(()) }
}
mod serde_yaml {
    pub fn from_str<T>(_data: &str) -> Result<T, ()> { Err(()) }
}
mod toml {
    pub fn from_str<T>(_data: &str) -> Result<T, ()> { Err(()) }
}
mod serde_pickle {
    pub fn from_slice<T>(_data: &[u8], _options: ()) -> Result<T, ()> { Err(()) }
}
mod ron { pub mod de { pub fn from_str<T>(_data: &str) -> Result<T, ()> { Err(()) } } }
mod ciborium {
    pub fn from_reader<T, R: std::io::Read>(_reader: R) -> Result<T, ()> { Err(()) }
}

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

fn false_negative_expansion_rust_deser<R: std::io::Read>(reader: R, input_reader: R, user_data: &[u8], user_str: &str) {
    let _: Result<User, ()> = serde_json::from_reader(reader);
    serde_pickle::from_slice(user_data, Default::default());
    ron::de::from_str(user_str);
    let _: Result<User, ()> = ciborium::from_reader(user_data);
    let _: Result<User, ()> = rmp_serde::from_read(input_reader);
}

fn main() {}
