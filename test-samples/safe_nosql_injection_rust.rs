use mongodb::{Client, Collection};
use mongodb::bson::{doc, Document};

// 负样本 - 使用固定字段和类型转换
pub async fn safe_fixed_filter(collection: &Collection<Document>, email: &str) {
    collection.find(doc! { "email": email.to_string() }).await;
}

// 负样本 - 使用允许名单验证字段名
pub async fn safe_allowlisted_field(collection: &Collection<Document>, field: &str, value: &str) {
    let allowed_fields: std::collections::HashSet<&str> = ["email", "status", "role"].iter().cloned().collect();
    if !allowed_fields.contains(field) {
        panic!("invalid field");
    }
    collection.find(doc! { field: value.to_string() }).await;
}

// 负样本 - 显式构造查询（不使用动态字段）
pub async fn safe_typed_query(collection: &Collection<Document>, username: &str, password: &str) {
    collection.find(doc! {
        "username": username.to_string(),
        "password": password.to_string()
    }).await;
}

// 负样本 - count_documents 使用固定字段
pub async fn safe_count_documents(collection: &Collection<Document>, status: &str) {
    collection.count_documents(doc! { "status": status.to_string() }).await;
}

// 负样本 - aggregate 使用硬编码 pipeline
pub async fn safe_aggregate(collection: &Collection<Document>) {
    let pipeline = vec![
        doc! { "$match": { "status": "active" } },
        doc! { "$group": { "_id": "$category", "count": { "$sum": 1 } } }
    ];
    collection.aggregate(pipeline).await;
}

// 负样本 - 静态 doc! 宏构造
pub async fn safe_static_doc(collection: &Collection<Document>, user_id: &str) {
    let filter = doc! { "user_id": user_id.to_string() };
    collection.find(filter).await;
}

// 负样本 - 使用强类型结构体
pub async fn safe_struct_query(collection: &Collection<Document>, username: String) {
    collection.find(doc! { "username": username }).await;
}
