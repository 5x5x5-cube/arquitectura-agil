import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "default-secret-key"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "postgresql://user:password@db:5432/orders"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
