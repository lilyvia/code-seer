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
