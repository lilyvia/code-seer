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
        jdbc.query(String.format("SELECT * FROM users WHERE name = '%s'", name), (rs, rowNum) -> rs.getString("name"));
        jdbc.update(String.format("UPDATE users SET name = '%s' WHERE id = %s", name, userId));
        jdbc.execute(String.format("DELETE FROM users WHERE id = %s", userId));
        jdbc.query(new StringBuilder().append("SELECT * FROM users WHERE id = ").append(userId).toString(), (rs, rowNum) -> rs.getString("name"));
        jdbc.update(new StringBuilder().append("UPDATE users SET name = '").append(name).append("' WHERE id = ").append(userId).toString());
        jdbc.execute(new StringBuilder().append("DELETE FROM users WHERE id = ").append(userId).toString());
        jdbc.query("SELECT * FROM users WHERE id = ".concat(userId), (rs, rowNum) -> rs.getString("name"));
        jdbc.update("UPDATE users SET name = '".concat(name).concat("' WHERE id = ").concat(userId));
        jdbc.execute("DELETE FROM users WHERE id = ".concat(userId));
    }

    public void vulnerableJpa(EntityManager em, String userId, String name) {
        em.createNativeQuery("SELECT * FROM users WHERE id = " + userId);
        em.createQuery("SELECT u FROM User u WHERE u.name = '" + name + "'");
        em.createNativeQuery(String.format("SELECT * FROM users WHERE name = '%s'", name));
        em.createQuery(String.format("SELECT u FROM User u WHERE u.id = %s", userId));
        em.createNativeQuery(new StringBuilder().append("SELECT * FROM users WHERE id = ").append(userId).toString());
        em.createQuery(new StringBuilder().append("SELECT u FROM User u WHERE u.name = '").append(name).append("'").toString());
        em.createNativeQuery("SELECT * FROM users WHERE id = ".concat(userId));
        em.createQuery("SELECT u FROM User u WHERE u.name = '".concat(name).concat("'"));
    }
}

interface VulnerableRepository {
    @Query(nativeQuery = true, value = "SELECT * FROM users WHERE id = " + "1")
    Object nativeQueryConcat();

    @Query(nativeQuery = true, value = String.format("SELECT * FROM users WHERE name = '%s'", "admin"))
    Object nativeQueryFormat();

    @Query(nativeQuery = true, value = new StringBuilder().append("SELECT * FROM users WHERE id = ").append("1").toString())
    Object nativeQueryStringBuilder();

    @Query(nativeQuery = true, value = "SELECT * FROM users WHERE id = ".concat("1"))
    Object nativeQueryConcatMethod();
}

class FalseNegativeExpansionSqlJava {
    void false_negative_expansion_hibernate(org.hibernate.Session session, String userId) {
        session.createSQLQuery("SELECT * FROM users WHERE id = " + userId).list();
    }
    void false_negative_expansion_jdbc(org.springframework.jdbc.core.JdbcTemplate jdbc, String userId) {
        jdbc.queryForObject("SELECT name FROM users WHERE id = " + userId, String.class);
        jdbc.queryForList("SELECT * FROM users WHERE id = " + userId);
    }
}
