package main

import (
	"context"
	"errors"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

// 负样本 - 使用固定字段和类型转换
func safeFixedFilter(collection *mongo.Collection, ctx context.Context, email string) {
	collection.Find(ctx, bson.M{"email": string(email)})
}

// 负样本 - 使用允许名单验证字段名
func safeAllowlistedField(collection *mongo.Collection, ctx context.Context, field string, value string) error {
	allowedFields := map[string]bool{"email": true, "status": true, "role": true}
	if !allowedFields[field] {
		return errors.New("invalid field")
	}
	collection.Find(ctx, bson.M{field: string(value)})
	return nil
}

// 负样本 - 显式构造查询（不使用动态字段）
func safeTypedQuery(collection *mongo.Collection, ctx context.Context, username string, password string) {
	collection.Find(ctx, bson.M{
		"username": string(username),
		"password": string(password),
	})
}

// 负样本 - CountDocuments 使用固定字段
func safeCountDocuments(collection *mongo.Collection, ctx context.Context, status string) {
	collection.CountDocuments(ctx, bson.M{"status": string(status)})
}

// 负样本 - aggregate 使用硬编码 pipeline
func safeAggregate(collection *mongo.Collection, ctx context.Context) {
	pipeline := mongo.Pipeline{
		{{Key: "$match", Value: bson.M{"status": "active"}}},
		{{Key: "$group", Value: bson.M{"_id": "$category", "count": bson.M{"$sum": 1}}}},
	}
	collection.Aggregate(ctx, pipeline)
}

// 负样本 - 静态 bson.M 构造
func safeStaticBsonM(collection *mongo.Collection, ctx context.Context, userId string) {
	filter := bson.M{"user_id": string(userId)}
	collection.Find(ctx, filter)
}

// 负样本 - 使用结构体绑定
func safeStructBinding(collection *mongo.Collection, ctx context.Context) {
	type Query struct {
		Username string `json:"username"`
		Email    string `json:"email"`
	}
	var q Query
	// 假设已通过 json.Unmarshal 解析
	collection.Find(ctx, bson.M{"username": q.Username})
}
