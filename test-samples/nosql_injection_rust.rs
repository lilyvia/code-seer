use mongodb::{Client, Collection};
use mongodb::bson::{doc, Document};
use serde_json;

// 正样本 - $where 表达式注入
pub async fn vulnerable_where_expression(collection: &Collection<Document>, expr: &str) {
    collection.find(doc! { "$where": expr }).await;
}

// 正样本 - find_one $where 注入
pub async fn vulnerable_where_find_one(collection: &Collection<Document>, expr: &str) {
    collection.find_one(doc! { "$where": expr }).await;
}

// 正样本 - count_documents $where 注入
pub async fn vulnerable_where_count(collection: &Collection<Document>, expr: &str) {
    collection.count_documents(doc! { "$where": expr }).await;
}

// 正样本 - 动态构造 filter（insert）
pub async fn vulnerable_dynamic_filter_insert(collection: &Collection<Document>, field: &str, value: &str) {
    let mut filter = doc! {};
    filter.insert(field, value);
    collection.find(filter).await;
}

// 正样本 - 直接从 JSON 解析 filter
pub async fn vulnerable_json_filter(collection: &Collection<Document>, json_filter: &str) {
    let filter: Document = serde_json::from_str(json_filter).unwrap();
    collection.find(filter).await;
}

// 正样本 - aggregate pipeline 注入
pub async fn vulnerable_aggregate(collection: &Collection<Document>, pipeline_json: &str) {
    let pipeline: Vec<Document> = serde_json::from_str(pipeline_json).unwrap();
    collection.aggregate(pipeline).await;
}

// 正样本 - 字符串拼接 $where
pub async fn vulnerable_where_concat(collection: &Collection<Document>, username: &str) {
    let where_expr = format!("this.username == '{}'", username);
    collection.find(doc! { "$where": where_expr }).await;
}
