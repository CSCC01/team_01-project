import os

DEBUG = True

SECRET_KEY = "fortestpurpose"

# # Prod
#
# SQLALCHEMY_DATABASE_URI = "postgres://cyhreifgcgqfbp:9a70ab4a858015cbeafdcdab9f69729b30f0c511c4c5aa65b9eb9f86afaaf8b6@ec2-184-72-236-3.compute-1.amazonaws.com:5432/dopb1f7u81aml"
# SQLALCHEMY_TRACK_MODIFICATIONS = True


# # Test
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'demo_07'
# USERNAME = 'root'
# PASSWORD = '12345678'
# DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
# SQLALCHEMY_TRACK_MODIFICATIONS = True

# Unit
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'test_2'
# USERNAME = 'root'
# PASSWORD = '12345678'
# TESTING = True
# SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_TRACK_MODIFICATIONS = True


# # TestDB
#
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True