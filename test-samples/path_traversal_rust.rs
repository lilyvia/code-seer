use std::fs::File;
use std::path::{Path, PathBuf};

fn test_path_traversal(user_input: &str) {
    let _ = File::open(user_input);
    let _ = std::fs::File::open(user_input);
    let _ = std::fs::remove_file(user_input);
    let _ = std::fs::remove_dir_all(user_input);
    let _ = tokio::fs::File::open(user_input);
    let _ = tokio::fs::remove_file(user_input);
    let _ = Path::new(user_input);
    let _ = PathBuf::from(user_input);
    let _ = std::fs::read(user_input);
    let _ = std::fs::write(user_input, b"data");
}

async fn false_negative_expansion_path_rust(user_path: String) {
    fs::copy(&user_path, "/tmp/out");
    fs::rename(&user_path, "/tmp/out");
    fs::create_dir_all(&user_path);
    tokio::fs::read_dir(&user_path).await;
}
