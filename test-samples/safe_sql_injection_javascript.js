function safeMySQL(conn, userId) {
    conn.query("SELECT * FROM users WHERE id = ?", [userId]);
}

function safePostgres(db, userId) {
    db.query("SELECT * FROM users WHERE id = $1", [userId]);
}

function safeSequelize(User, userId) {
    User.findByPk(userId);
    User.findOne({ where: { id: userId } });
}

function safeKnex(knex, name) {
    knex.raw("SELECT * FROM products WHERE name = ?", [name]);
}

function safePrisma(prisma, input) {
    prisma.$queryRaw`SELECT * FROM logs WHERE msg = ${input}`;
    prisma.$executeRaw`DELETE FROM sessions WHERE id = ${input}`;
}

function safeSequelizeParam(sequelize, userId) {
    sequelize.query("SELECT * FROM users WHERE id = ?", { replacements: [userId] });
}

function safeKnexBuilder(knex, name) {
    knex("products").where({ name: name });
}

function safePrismaOrm(prisma, input) {
    prisma.log.findMany({ where: { msg: input } });
}

function safeFalseNegativeExpansion(pool, input) {
    // Safe: pg parameterized query separates SQL text from user data.
    return pool.query('SELECT * FROM users WHERE name = $1', [input]);
}
