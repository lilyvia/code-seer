mod sqlx {
    pub struct Query<'a> {
        sql: &'a str,
    }

    pub fn query_as(sql: &str) -> Query<'_> {
        Query { sql }
    }

    impl<'a> Query<'a> {
        pub fn bind(self, value: i32) -> Self {
            let _ = (self.sql, value);
            self
        }
    }
}

fn safe_sqli(id: i32) {
    let prepared = sqlx::query_as;
    let _statement = prepared("SELECT * FROM users WHERE id = $1").bind(id);
}

fn main() {}
