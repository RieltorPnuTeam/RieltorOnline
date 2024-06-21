# config.py
import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'aboba'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'abobaaaa'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/rieltoronline'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
