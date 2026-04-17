import java.sql.Connection;
import java.sql.Statement;
import org.springframework.jdbc.core.JdbcTemplate;
import javax.persistence.EntityManager;
import javax.persistence.Query;
import org.springframework.data.jpa.repository.Query;

public class SqliJava {
    public void vulnerable(Connection conn, String userId, String name) throws Exception {
        Statement stmt = conn.createStatement();
        stmt.executeQuery("SELECT * FROM users WHERE id = " + userId);
        stmt.execute("SELECT * FROM users WHERE id = " + userId);
        stmt.executeQuery(String.format("SELECT * FROM users WHERE name = '%s'", name));
        stmt.executeQuery(new StringBuilder().append("SELECT * FROM users WHERE id = ").append(userId).toString());
    }

    public void vulnerableJdbcTemplate(JdbcTemplate jdbc, String userId, String name) {
        jdbc.query("SELECT * FROM users WHERE id = " + userId, (rs, rowNum) -> rs.getString("name"));
        jdbc.update("UPDATE users SET name = '" + name + "' WHERE id = " + userId);
        jdbc.execute("DELETE FROM users WHERE id = " + userId);
    }

    public void vulnerableJpa(EntityManager em, String userId, String name) {
        em.createNativeQuery("SELECT * FROM users WHERE id = " + userId);
        em.createQuery("SELECT u FROM User u WHERE u.name = '" + name + "'");
        em.createNativeQuery(String.format("SELECT * FROM users WHERE name = '%s'", name));
        em.createQuery(String.format("SELECT u FROM User u WHERE u.id = %s", userId));
    }
}

interface VulnerableRepository {
    @Query(nativeQuery = true, value = "SELECT * FROM users WHERE id = " + "1")
    Object nativeQueryConcat();

    @Query(nativeQuery = true, value = String.format("SELECT * FROM users WHERE name = '%s'", "admin"))
    Object nativeQueryFormat();
}
