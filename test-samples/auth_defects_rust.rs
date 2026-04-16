use axum::extract::Path;

async fn get_user(Path(id): Path<i32>, db: Extension<Database>) -> Json<User> {
    let user = sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(id)
        .fetch_one(&db)
        .await
        .unwrap();
    Json(user)
}

async fn update_post(Path((id, slug)): Path<(i32, String)>, db: Extension<Database>) -> Json<Post> {
    let post = sqlx::query("UPDATE posts SET title = $1 WHERE id = $2")
        .bind(slug)
        .bind(id)
        .execute(&db)
        .await
        .unwrap();
    Json(post)
}

async fn delete_order(Path(order_id): Path<i32>, db: Extension<Database>) -> StatusCode {
    let _ = sqlx::query("DELETE FROM orders WHERE id = $1")
        .bind(order_id)
        .execute(&db)
        .await;
    StatusCode::OK
}

async fn get_item(Path(id): Path<i32>, client: Client) -> Json<Item> {
    let row = client.query("SELECT * FROM items WHERE id = $1", &[&id]).await.unwrap();
    Json(row)
}
