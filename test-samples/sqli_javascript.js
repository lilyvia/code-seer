function vulnerableSQLi(conn, userId) {
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    conn.query(query);
}
