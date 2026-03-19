import java.sql.Connection;
import java.sql.Statement;

public class SqliJava {
    public void vulnerable(Connection conn, String userId, String name) throws Exception {
        Statement stmt = conn.createStatement();
        stmt.executeQuery("SELECT * FROM users WHERE id = " + userId);
        stmt.execute("SELECT * FROM users WHERE id = " + userId);
        stmt.executeQuery(String.format("SELECT * FROM users WHERE name = '%s'", name));
        stmt.executeQuery(new StringBuilder().append("SELECT * FROM users WHERE id = ").append(userId).toString());
    }
}
