# config.py

class Config:
    SECRET_KEY = 'aboba'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost/rieltoronline'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
