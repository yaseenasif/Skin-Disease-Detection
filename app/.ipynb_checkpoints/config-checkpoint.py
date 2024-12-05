import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqlconnector://root:root@localhost/skin_disease'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
