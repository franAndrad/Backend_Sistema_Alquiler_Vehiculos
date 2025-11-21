import pymysql
import urllib.parse


class DBInitializer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBInitializer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def init_database(self, uri):
        parsed = urllib.parse.urlparse(uri)

        user = parsed.username
        password = parsed.password
        host = parsed.hostname
        database = parsed.path.replace("/", "")

        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            autocommit=True
        )

        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
        cur.close()
        conn.close()

    def init_tables(self, app, db):
        with app.app_context():
            db.create_all()
