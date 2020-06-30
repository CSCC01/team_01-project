import os

DEBUG = True

SECRET_KEY = os.urandom(24)

# Prod

SQLALCHEMY_DATABASE_URI = "postgres://acakkhlblzjgdn:380973a230519b862a2e3b44923629e394f5ab8db48a1225b940030cd2df853f@ec2-54-161-208-31.compute-1.amazonaws.com:5432/d5skqebio5o5p9"
SQLALCHEMY_TRACK_MODIFICATIONS = True


# Test
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'demo_05'
# USERNAME = 'root'
# PASSWORD = '12345678'
# DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = True




