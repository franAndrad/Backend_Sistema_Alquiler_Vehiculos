import os

class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_EXPIRES_IN", "900"))

    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.mailtrap.io")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "2525"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
