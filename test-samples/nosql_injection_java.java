import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import javax.servlet.http.HttpServletRequest;

public class NosqlInjectionJava {
    // 正样本 - $where 表达式注入
    public void vulnerableWhereExpression(MongoCollection<Document> collection, String expr) {
        collection.find(new Document("$where", expr));
    }

    // 正样本 - findOne $where 注入
    public void vulnerableWhereFindOne(MongoCollection<Document> collection, String expr) {
        collection.find(new Document("$where", expr)).first();
    }

    // 正样本 - countDocuments $where 注入
    public void vulnerableWhereCount(MongoCollection<Document> collection, String expr) {
        collection.countDocuments(new Document("$where", expr));
    }

    // 正样本 - 动态构造 filter（通过 put）
    public void vulnerableDynamicFilterPut(MongoCollection<Document> collection, HttpServletRequest req) {
        Document filter = new Document();
        filter.put(req.getParameter("field"), req.getParameter("value"));
        collection.find(filter);
    }

    // 正样本 - 动态构造 filter（直接传入 request 参数）
    public void vulnerableDynamicFilterDirect(MongoCollection<Document> collection, HttpServletRequest req) {
        Document filter = new Document();
        filter.put(req.getParameter("field"), req.getParameter("value"));
        collection.find(filter);
    }

    // 正样本 - aggregate pipeline 注入
    public void vulnerableAggregate(MongoCollection<Document> collection, String matchStage) {
        Document pipeline = Document.parse(matchStage);
        collection.aggregate(java.util.Arrays.asList(pipeline));
    }

    // 正样本 - 字符串拼接 $where
    public void vulnerableWhereConcat(MongoCollection<Document> collection, String username) {
        String whereExpr = "this.username == '" + username + "'";
        collection.find(new Document("$where", whereExpr));
    }

    // 正样本 - BasicDBObject 动态构造
    public void vulnerableBasicDBObject(com.mongodb.BasicDBObject query, HttpServletRequest req) {
        query.put(req.getParameter("key"), req.getParameter("val"));
    }
}
