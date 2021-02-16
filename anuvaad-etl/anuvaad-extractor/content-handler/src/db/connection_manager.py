from config import MONGO_CONNECTION_URL,MONGO_DB_SCHEMA
from config import REDIS_SERVER_HOST,REDIS_SERVER_PORT
from pymongo import MongoClient
from anuvaad_auditor.loghandler import log_info, log_exception
from utilities import AppContext
from flask import g
import redis
client = MongoClient(MONGO_CONNECTION_URL)

def get_db():
    return client[MONGO_DB_SCHEMA]


def get_redis():
    if 'redisdb' not in g:
        log_info("Establishing connection with redis store", AppContext.getContext())
        g.redisdb = redis.Redis(host=REDIS_SERVER_HOST, port=REDIS_SERVER_PORT, db=4)
    return g.redisdb

