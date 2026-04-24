mod sqlx {
    pub struct Query<T>(pub std::marker::PhantomData<T>);

    pub fn query(sql: &str) -> Query<()> {
        let _ = sql;
        Query(std::marker::PhantomData)
    }

    pub fn query_as<T>(sql: &str) -> Query<T> {
        let _ = sql;
        Query(std::marker::PhantomData)
    }
}

mod diesel {
    pub fn sql_query(sql: String) {
        let _ = sql;
    }
}

mod tokio_postgres {
    pub struct Client;
    pub struct Statement;

    impl Client {
        pub fn query(&self, sql: &str, params: &[&str]) {
            let _ = (sql, params);
        }
    }

    impl Statement {
        pub fn from(sql: String) -> Self {
            let _ = sql;
            Self
        }
    }
}

mod rusqlite {
    pub struct Connection;

    impl Connection {
        pub fn execute(&self, sql: String, params: &[&str]) {
            let _ = (sql, params);
        }
    }
}

struct User;

struct Conn;

impl Conn {
    fn execute(&self, sql: String) {
        let _ = sql;
    }
}

fn test_sqli(user_input: &str, user_id: i32) {
    let conn = Conn;
    let client = tokio_postgres::Client;

    let _ = sqlx::query(&format!("SELECT * FROM users WHERE id = {}", user_id));

    let query2 = "SELECT * FROM users WHERE name = ".to_string() + user_input;
    conn.execute(query2);

    client.query(&format!("DELETE FROM posts WHERE id = {}", user_input), &[]);

    let _stmt = tokio_postgres::Statement::from(
        "SELECT * FROM users WHERE id = ".to_string() + user_input,
    );

    conn.execute(format!("INSERT INTO logs VALUES ('{}')", user_input));
}

fn false_negative_expansion_sqlx(client: tokio_postgres::Client, user_id: String) {
    let user_sql = format!("SELECT * FROM users WHERE id = {}", user_id);
    diesel::sql_query(user_sql.clone());
    client.query(&user_sql, &[]);

    let _: sqlx::Query<User> = sqlx::query_as(&format!(
        "SELECT * FROM users WHERE id = {}",
        user_id,
    ));
}

fn false_negative_expansion_rusqlite(user_id: String) {
    let rusqlite_conn = rusqlite::Connection;
    rusqlite_conn.execute(
        format!("SELECT * FROM users WHERE id = {}", user_id),
        &[],
    );
}

fn main() {}
