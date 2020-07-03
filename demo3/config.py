import os

DEBUG = True

SECRET_KEY = "fortestpurpose"

# Prod

SQLALCHEMY_DATABASE_URI = "postgres://lgnkcdbgatieto:160de1e4608e742d855530f31fe74ce18ad910ab7990c5d635fd09770ca5ee4b@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d89pqc3jvvkrlp"
SQLALCHEMY_TRACK_MODIFICATIONS = True


# # Test
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'demo_06'
# USERNAME = 'root'
# PASSWORD = '12345678'
# DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = True
