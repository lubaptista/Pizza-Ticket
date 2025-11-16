import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("JWT_SECRET", "jwt-secret"))

    # Se DATABASE_URL existir -> usar Postgres (docker)
    # Se não -> usar SQLite (ambiente de desenvolvimento)
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        # SQLite local
        DATABASE_URL = "sqlite:///pizzaria.db"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
