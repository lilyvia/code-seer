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


class Session:
    def __init__(self, engine):
        self.engine = engine

    def execute(self, *args, **kwargs):
        return args, kwargs


connection = Connection()


def safe_queries(user_id, user_name):
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    engine = create_engine("sqlite://")
    session = Session(engine)

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    User.objects.raw("SELECT * FROM auth_user WHERE username = %s", [user_name])
    User.objects.extra(where=["username = %s"], params=[user_name])
    connection.cursor().execute("SELECT * FROM users WHERE id = %s", [user_id])
    session.execute(text("SELECT * FROM accounts WHERE owner = :owner"), {"owner": user_name})
    session.execute(text("SELECT * FROM accounts WHERE id = :user_id"), {"user_id": user_id})
