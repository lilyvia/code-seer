using MongoDB.Bson;
using MongoDB.Driver;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;

public class SafeNosqlInjectionCSharp
{
    // 负样本 - 使用固定字段和类型转换
    public void SafeFixedFilter(IMongoCollection<BsonDocument> collection, string email)
    {
        collection.Find(new BsonDocument("email", email.ToString()));
    }

    // 负样本 - 使用允许名单验证字段名
    public void SafeAllowlistedField(IMongoCollection<BsonDocument> collection, HttpRequest request)
    {
        var allowedFields = new HashSet<string> { "email", "status", "role" };
        var field = request.Query["field"].ToString();
        if (!allowedFields.Contains(field))
        {
            throw new ArgumentException("invalid field");
        }
        collection.Find(new BsonDocument(field, request.Query["value"].ToString()));
    }

    // 负样本 - 使用 Filter 构建器（类型安全）
    public void SafeFilterBuilder(IMongoCollection<BsonDocument> collection, string username, string password)
    {
        var filter = Builders<BsonDocument>.Filter.And(
            Builders<BsonDocument>.Filter.Eq("username", username),
            Builders<BsonDocument>.Filter.Eq("password", password)
        );
        collection.Find(filter);
    }

    // 负样本 - CountDocuments 使用固定字段
    public void SafeCountDocuments(IMongoCollection<BsonDocument> collection, string status)
    {
        collection.CountDocuments(new BsonDocument("status", status.ToString()));
    }

    // 负样本 - aggregate 使用硬编码 pipeline
    public void SafeAggregate(IMongoCollection<BsonDocument> collection)
    {
        var pipeline = new[]
        {
            new BsonDocument("$match", new BsonDocument("status", "active")),
            new BsonDocument("$group", new BsonDocument("_id", "$category"))
        };
        collection.Aggregate(pipeline);
    }

    // 负样本 - 静态 BsonDocument 构造
    public void SafeStaticDocument(IMongoCollection<BsonDocument> collection, string userId)
    {
        var filter = new BsonDocument();
        filter["userId"] = userId.ToString();
        collection.Find(filter);
    }
}
