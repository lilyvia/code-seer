package main

import (
	"context"
	"encoding/json"
	"net/http"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

// 正样本 - $where 表达式注入
func vulnerableWhereExpression(collection *mongo.Collection, ctx context.Context, expr string) {
	collection.Find(ctx, bson.M{"$where": expr})
}

// 正样本 - FindOne $where 注入
func vulnerableWhereFindOne(collection *mongo.Collection, ctx context.Context, expr string) {
	collection.FindOne(ctx, bson.M{"$where": expr})
}

// 正样本 - CountDocuments $where 注入
func vulnerableWhereCount(collection *mongo.Collection, ctx context.Context, expr string) {
	collection.CountDocuments(ctx, bson.M{"$where": expr})
}

// 正样本 - 动态构造 filter（map 赋值）
func vulnerableDynamicFilterMap(collection *mongo.Collection, ctx context.Context, r *http.Request) {
	filter := bson.M{}
	filter[r.FormValue("field")] = r.FormValue("value")
	collection.Find(ctx, filter)
}

// 正样本 - 直接使用请求体作为 filter
func vulnerableDirectBodyFilter(collection *mongo.Collection, ctx context.Context, body []byte) {
	var filter bson.M
	json.Unmarshal(body, &filter)
	collection.Find(ctx, filter)
}

// 正样本 - aggregate pipeline 注入
func vulnerableAggregate(collection *mongo.Collection, ctx context.Context, pipeline []byte) {
	var stages []bson.D
	json.Unmarshal(pipeline, &stages)
	collection.Aggregate(ctx, stages)
}

// 正样本 - 字符串拼接 $where
func vulnerableWhereConcat(collection *mongo.Collection, ctx context.Context, username string) {
	whereExpr := "this.username == '" + username + "'"
	collection.Find(ctx, bson.M{"$where": whereExpr})
}

// 正样本 - bson.D 动态构造
func vulnerableBsonDDynamic(collection *mongo.Collection, ctx context.Context, r *http.Request) {
	filter := bson.D{
		{Key: r.FormValue("field"), Value: r.FormValue("value")},
	}
	collection.Find(ctx, filter)
}
