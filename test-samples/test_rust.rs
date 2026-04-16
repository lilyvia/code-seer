use std::process::Command;

fn test_sqli(user_input: &str, user_id: i32) {
    // SQL injection patterns
    sqlx::query(&format!("SELECT * FROM users WHERE id = {}", user_id)).bind(user_id).execute(&pool).await;

    let query2 = "SELECT * FROM users WHERE name = ".to_string() + user_input;
    conn.execute(&query2).await;

    client.query(&format!("DELETE FROM posts WHERE id = {}", user_input), &[]).await;

    let stmt = Statement::from("SELECT * FROM users WHERE id = ".to_string() + user_input);

    conn.execute(format!("INSERT INTO logs VALUES ('{}')", user_input));
}

fn test_cmd_exec(user_cmd: &str, args: Vec<&str>) {
    // Command execution patterns
    let _ = Command::new(user_cmd).output();
    let _ = Command::new(&user_cmd).arg("-l").spawn();
    let _ = Command::new(&user_cmd).args(&args).status();
    let _ = std::process::Command::new(user_cmd).output();
}

fn test_xss(name: &str) {
    // XSS patterns
    let html = format!("<div>{}</div>", name);
    let response = HttpResponse::Ok().body(format!("<h1>{}</h1>", name));
    let html2 = Html(format!("<script>alert('{}')</script>", name));
}
