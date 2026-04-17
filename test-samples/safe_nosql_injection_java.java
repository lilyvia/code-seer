import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;
import javax.servlet.http.HttpServletRequest;
import java.util.HashSet;
import java.util.Set;

public class SafeNosqlInjectionJava {
    // 负样本 - 使用固定字段和类型转换
    public void safeFixedFilter(MongoCollection<Document> collection, String email) {
        collection.find(new Document("email", String.valueOf(email)));
    }

    // 负样本 - 使用允许名单验证字段名
    public void safeAllowlistedField(MongoCollection<Document> collection, HttpServletRequest req) {
        Set<String> allowedFields = new HashSet<>();
        allowedFields.add("email");
        allowedFields.add("status");
        
        String field = req.getParameter("field");
        if (!allowedFields.contains(field)) {
            throw new IllegalArgumentException("invalid field");
        }
        
        collection.find(new Document(field, String.valueOf(req.getParameter("value"))));
    }

    // 负样本 - 使用 Filters 构建器（类型安全）
    public void safeFiltersBuilder(MongoCollection<Document> collection, String username, String password) {
        collection.find(com.mongodb.client.model.Filters.and(
            com.mongodb.client.model.Filters.eq("username", username),
            com.mongodb.client.model.Filters.eq("password", password)
        ));
    }

    // 负样本 - countDocuments 使用固定字段
    public void safeCountDocuments(MongoCollection<Document> collection, String status) {
        collection.countDocuments(new Document("status", String.valueOf(status)));
    }

    // 负样本 - aggregate 使用硬编码 pipeline
    public void safeAggregate(MongoCollection<Document> collection) {
        collection.aggregate(java.util.Arrays.asList(
            new Document("$match", new Document("status", "active")),
            new Document("$group", new Document("_id", "$category"))
        ));
    }

    // 负样本 - 静态 Document 构造
    public void safeStaticDocument(MongoCollection<Document> collection, String userId) {
        Document filter = new Document();
        filter.put("userId", String.valueOf(userId));
        collection.find(filter);
    }
}
