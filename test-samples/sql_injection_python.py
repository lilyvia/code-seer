import sqlite3


def text(query):
    return query


def create_engine(dsn):
    return Engine(dsn)


class Cursor:
    def execute(self, *args, **kwargs):
        return args, kwargs


class Connection:
    def cursor(self):
        return Cursor()


class RawManager:
    def raw(self, *args, **kwargs):
        return args, kwargs

    def extra(self, *args, **kwargs):
        return args, kwargs


class User:
    objects = RawManager()


class Engine:
    def __init__(self, dsn):
        self.dsn = dsn

    def execute(self, *args, **kwargs):
        return args, kwargs


class Session:
    def __init__(self, engine):
        self.engine = engine

    def execute(self, *args, **kwargs):
        return args, kwargs


connection = Connection()


def vulnerable(user_id, user_name):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    engine = create_engine("sqlite://")
    session = Session(engine)

    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)
    cursor.execute("SELECT * FROM users WHERE name = '{}'".format(user_name))
    cursor.execute("SELECT * FROM users WHERE id = " + user_id)
    User.objects.raw("SELECT * FROM auth_user WHERE username = '%s'" % user_name)
    User.objects.raw(f"SELECT * FROM auth_user WHERE id = {user_id}")
    User.objects.extra(where=["username = '%s'" % user_name])
    User.objects.extra(where=[f"id = {user_id}"])
    connection.cursor().execute(text(f"SELECT * FROM payments WHERE id = {user_id}"))
    session.execute(text("SELECT * FROM accounts WHERE owner = '" + user_name + "'"))
    session.execute(text("SELECT * FROM accounts WHERE id = %s" % user_id))
    engine.execute(text("SELECT * FROM audit_logs WHERE actor = '{}'".format(user_name)))
    engine.execute(text("SELECT * FROM audit_logs WHERE id = " + user_id))
    conn.execute(f"SELECT * FROM users WHERE name = {user_name}")
    conn.execute("SELECT * FROM users WHERE id = %s" % user_id)

def false_negative_expansion_pandas(pd, conn, user_id):
    user_sql = f"SELECT * FROM users WHERE id = {user_id}"
    return pd.read_sql(user_sql, conn)

async def false_negative_expansion_asyncpg(conn, user_id):
    user_query = f"SELECT * FROM users WHERE id = {user_id}"
    return await conn.fetch(user_query)
