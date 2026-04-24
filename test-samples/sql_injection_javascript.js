function vulnerableSQLi(conn, userId) {
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    conn.query(query);
}

function vulnerableSequelize(sequelize, userId) {
    sequelize.query("SELECT * FROM users WHERE id = " + userId);
}

function vulnerableKnex(knex, name) {
    knex.raw(`SELECT * FROM products WHERE name = ${name}`);
}

function vulnerablePrismaQueryRaw(prisma, input) {
    const sql = `SELECT * FROM logs WHERE msg = ${input}`;
    prisma.$queryRawUnsafe(sql);
}

function vulnerablePrismaExecuteRaw(prisma, input) {
    prisma.$executeRawUnsafe(`DELETE FROM sessions WHERE id = ${input}`);
}

function vulnerableSequelizeRawReplacements(sequelize, userId) {
    const sql = "SELECT * FROM users WHERE id = " + userId;
    sequelize.query(sql, { replacements: { id: userId } });
}

function vulnerableSequelizeRawBind(sequelize, name) {
    const sql = `SELECT * FROM users WHERE name = ${name}`;
    sequelize.query(sql, { bind: { name: name } });
}

function vulnerableModelSequelizeQuery(model, input) {
    const sql = "SELECT * FROM orders WHERE code = '" + input + "'";
    model.sequelize.query(sql);
}

function vulnerableKnexDbRaw(db, input) {
    db.raw(`SELECT * FROM items WHERE sku = ${input}`);
}

function vulnerablePrismaQueryRawTemplate(prisma, input) {
    prisma.$queryRawUnsafe(`SELECT * FROM events WHERE type = ${input}`);
}

function vulnerablePrismaExecuteRawVar(prisma, input) {
    const sql = "DELETE FROM tokens WHERE id = " + input;
    prisma.$executeRawUnsafe(sql);
}

function false_negative_expansion_typeorm(repo, userId) {
    const userSql = `SELECT * FROM users WHERE id = ${userId}`;
    repo.query(userSql);
}

function false_negative_expansion_mysql2(pool, input) {
    pool.execute("SELECT * FROM users WHERE name = '" + input + "'");
}

function false_negative_expansion_knex(knex, input) {
    knex.whereRaw(`name = ${input}`);
    knex.fromRaw("users where id = " + input);
}

function false_negative_expansion_typeorm_builder(repo, userId, request) {
    // Vulnerable: user-controlled template literal is passed into TypeORM where().
    repo.createQueryBuilder('user').where(`user.id = ${userId}`).getMany();
    repo.createQueryBuilder('user').where('user.name = ' + request.query.name, {});
}

function false_negative_expansion_pg_pool(pool, client, input) {
    // Vulnerable: SQL is concatenated before reaching pg query sinks.
    pool.query('SELECT * FROM users WHERE name = ' + input, []);
    client.query(`SELECT * FROM audit WHERE actor = ${input}`, []);
}
