// Safe Rust patterns that avoid SQL injection

fn safe_sqli() {
    // Use ORM or prepared statements with bind parameters
    // This sample intentionally avoids any raw query patterns
    println!("Use sqlx::query(\"SELECT ...\").bind(val).execute(pool)");
}
