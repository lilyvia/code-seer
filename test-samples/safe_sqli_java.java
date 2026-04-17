import java.sql.Connection;
import java.sql.PreparedStatement;
import org.springframework.jdbc.core.JdbcTemplate;
import javax.persistence.EntityManager;
import org.springframework.data.jpa.repository.Query;

public class SafeSqliJava {
    public void safePreparedStatement(Connection conn, String userId) throws Exception {
        PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
        ps.setString(1, userId);
        ps.executeQuery();
    }

    public void safeJdbcTemplate(JdbcTemplate jdbc, String userId) {
        jdbc.query("SELECT * FROM users WHERE id = ?", new Object[]{userId}, (rs, rowNum) -> rs.getString("name"));
        jdbc.update("UPDATE users SET name = ? WHERE id = ?", userId, 1);
        jdbc.execute("DELETE FROM users WHERE id = 1");
    }

    public void safeJpa(EntityManager em, String userId) {
        em.createNativeQuery("SELECT * FROM users WHERE id = :id").setParameter("id", userId);
        em.createQuery("SELECT u FROM User u WHERE u.id = :id").setParameter("id", userId);
    }
}

interface SafeRepository {
    @Query("SELECT u FROM User u WHERE u.id = :id")
    Object safeJpaQuery();

    @Query(nativeQuery = true, value = "SELECT * FROM users WHERE id = ?")
    Object safeNativeQuery();
}
