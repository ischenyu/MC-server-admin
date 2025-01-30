"""
author: Shan Chenyu (abb1234aabb@gmail.com)
Description: The config of the server.
"""

# Mysql connection config
class DB_Config(object):
    USER = "mc"
    PASSWORD = "Dingtalk1234561017"
    HOST = "192.168.1.2"
    PORT = 3306
    DB = "mc"

# Server run parameter config
class SERVER_Config(object):
    HOST = "0.0.0.0"
    PORT = 1222
    DEBUG = True
    TESTING = True
    SECRET_KEY = "GHD373%$GHDBSA*G(*BV"

# Redis connection config
class REDIS_Config(object):
    HOST = "localhost"
    PORT = 6379
    DB = 0
    PASSWORD = "Dingtalk1234561017"

