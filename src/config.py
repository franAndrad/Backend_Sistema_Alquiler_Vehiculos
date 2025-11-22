import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:11111010fa@localhost/tp"
    )

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes