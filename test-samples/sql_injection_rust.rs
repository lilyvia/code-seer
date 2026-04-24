use sqlx;
use tokio_postgres::{Client, Statement};

fn test_sqli(user_input: &str, user_id: i32) {
    // SQL injection patterns
    sqlx::query(&format!("SELECT * FROM users WHERE id = {}", user_id)).bind(user_id).execute(&pool).await;

    let query2 = "SELECT * FROM users WHERE name = ".to_string() + user_input;
    conn.execute(&query2).await;

    client.query(&format!("DELETE FROM posts WHERE id = {}", user_input), &[]).await;

    let stmt = Statement::from("SELECT * FROM users WHERE id = ".to_string() + user_input);

    conn.execute(format!("INSERT INTO logs VALUES ('{}')", user_input));
}

fn false_negative_expansion_diesel(client: Client, user_id: String) {
    let user_sql = format!("SELECT * FROM users WHERE id = {}", user_id);
    diesel::sql_query(user_sql.clone());
    client.query(&user_sql, &[]);
}
