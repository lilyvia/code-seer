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
