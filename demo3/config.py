import os

DEBUG = True

SECRET_KEY = "fortestpurpose"

# Prod

SQLALCHEMY_DATABASE_URI = "postgres://xtpzdivlvyzaee:36aec330f168895db86c243aed33e457239fd8d9ac077c5755ce56bce1a0be1c@ec2-54-159-138-67.compute-1.amazonaws.com:5432/d8l356lt99vu5d"
SQLALCHEMY_TRACK_MODIFICATIONS = True


# # Test
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'demo_05'
# USERNAME = 'root'
# PASSWORD = '12345678'
# DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = True
