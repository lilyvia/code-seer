import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.Collections;

class SafeSqliJava {
    public void safePreparedStatement(Connection conn, String userId) throws Exception {
        PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
        ps.setString(1, userId);
        ps.executeQuery();
    }

    public void safeJdbcTemplate(JdbcTemplate jdbc, String userId) {
        jdbc.query("SELECT * FROM users WHERE id = ?", new Object[]{userId}, (rs, rowNum) -> rs.getString("name"));
        jdbc.update("UPDATE users SET name = ? WHERE id = ?", userId, 1);
        jdbc.execute("DELETE FROM users WHERE id = 1");
        jdbc.queryForObject("SELECT name FROM users WHERE id = ?", String.class, userId);
        jdbc.batchUpdate("UPDATE users SET name = ? WHERE id = ?", java.util.Collections.singletonList(new Object[]{userId, 1}));
    }

    public void safeJpa(EntityManager em, String userId) {
        em.createNativeQuery("SELECT * FROM users WHERE id = :id").setParameter("id", userId);
        em.createQuery("SELECT u FROM User u WHERE u.id = :id").setParameter("id", userId);
        em.createNativeQuery("SELECT * FROM users WHERE id = ?").setParameter(1, userId);
        em.createQuery("SELECT u FROM User u WHERE u.id = ?1").setParameter(1, userId);
    }
}

class SafeAdditionalOrmSqlJava {
    void safeNamedParameter(NamedParameterJdbcTemplate jdbc, String userId) {
        jdbc.query("SELECT * FROM users WHERE id = :id", Collections.singletonMap("id", userId));
    }

    void safeHibernate(Session session, String userId) {
        session.createQuery("FROM User WHERE id = :id");
    }
}

class JdbcTemplate {
    Object query(String sql, Object[] args, RowMapper mapper) { return null; }
    int update(String sql, Object... args) { return 0; }
    void execute(String sql) {}
    Object queryForObject(String sql, Class<?> type, Object... args) { return null; }
    void batchUpdate(String sql, java.util.List<Object[]> args) {}
}

interface RowMapper { Object map(Row rs, int rowNum); }
class Row { String getString(String name) { return ""; } }
class NamedParameterJdbcTemplate { Object query(String sql, Object args) { return null; } }
class EntityManager { QueryObject createNativeQuery(String sql) { return new QueryObject(); } QueryObject createQuery(String sql) { return new QueryObject(); } }
class QueryObject { QueryObject setParameter(String name, String value) { return this; } QueryObject setParameter(int index, String value) { return this; } }
@interface Query { String value() default ""; boolean nativeQuery() default false; }
class Session { Object createQuery(String hql) { return null; } }

interface SafeRepository {
    @Query("SELECT u FROM User u WHERE u.id = :id")
    Object safeJpaQuery();

    @Query(nativeQuery = true, value = "SELECT * FROM users WHERE id = ?")
    Object safeNativeQuery();

    @Query("SELECT u FROM User u WHERE u.name = ?1")
    Object safeJpaQueryPositional();

    @Query(nativeQuery = true, value = "SELECT * FROM users WHERE id = :id")
    Object safeNativeQueryNamed();
}
