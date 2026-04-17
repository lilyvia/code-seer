using MongoDB.Bson;
using MongoDB.Driver;
using Microsoft.AspNetCore.Http;

public class NosqlInjectionCSharp
{
    // 正样本 - $where 表达式注入
    public void VulnerableWhereExpression(IMongoCollection<BsonDocument> collection, string expr)
    {
        collection.Find(new BsonDocument("$where", expr));
    }

    // 正样本 - FindOne $where 注入
    public void VulnerableWhereFindOne(IMongoCollection<BsonDocument> collection, string expr)
    {
        collection.Find(new BsonDocument("$where", expr)).FirstOrDefault();
    }

    // 正样本 - CountDocuments $where 注入
    public void VulnerableWhereCount(IMongoCollection<BsonDocument> collection, string expr)
    {
        collection.CountDocuments(new BsonDocument("$where", expr));
    }

    // 正样本 - 动态构造 filter（索引赋值）
    public void VulnerableDynamicFilterIndex(IMongoCollection<BsonDocument> collection, HttpRequest request)
    {
        var filter = new BsonDocument();
        filter[request.Query["field"]] = request.Query["value"];
        collection.Find(filter);
    }

    // 正样本 - 直接使用请求体作为 filter
    public void VulnerableDirectBodyFilter(IMongoCollection<BsonDocument> collection, string jsonFilter)
    {
        var filter = BsonDocument.Parse(jsonFilter);
        collection.Find(filter);
    }

    // 正样本 - aggregate pipeline 注入
    public void VulnerableAggregate(IMongoCollection<BsonDocument> collection, string pipelineJson)
    {
        var pipeline = BsonDocument.Parse(pipelineJson);
        collection.Aggregate(new[] { pipeline });
    }

    // 正样本 - 字符串拼接 $where
    public void VulnerableWhereConcat(IMongoCollection<BsonDocument> collection, string username)
    {
        var whereExpr = $"this.username == '{username}'";
        collection.Find(new BsonDocument("$where", whereExpr));
    }

    // 正样本 - FilterDefinition 注入
    public void VulnerableFilterDefinition(IMongoCollection<BsonDocument> collection, string filterStr)
    {
        var filter = BsonDocument.Parse(filterStr);
        collection.Find(filter);
    }
}
