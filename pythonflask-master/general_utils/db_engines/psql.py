from config import Config
from sqlalchemy import create_engine

#psql engine creation stuff goes here

def make_engine():
    create_engine(Config.SQLALCHEMY_DATABASE_URI,pool_pre_ping=Config.SQLALCHEMY_POOL_PRE_PING,pool_size=Config.SQLALCHEMY_POOL_SIZE,max_overflow=Config.SQLALCHEMY_MAX_OVERFLOW)
