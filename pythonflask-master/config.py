from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy import create_engine
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(verbose=True, dotenv_path=env_path)
import os


class Config:
    """
    config class for env parsing
    """
    # PORT = os.getenv('PORT')
    DEBUG = True
    #to be user with any hashing salting usecases through out the application
    SECRET_KEY = 'BSVIiuYZcTAzHRe07NzEgYqveb6mqwsa' 
    REFRESH_SECRET_KEY='611E7F5B77154'
    #To Be attached under the general library
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    FIXED_RATE = 200
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_PRE_PING = True
    SQLALCHEMY_POOL_RECYCLE = 300
    GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_SCRECT_KEY')
    #JWT BLOCK
    JWT_ALGORITHM  = os.getenv('JWT_ALGORITHM')
    JWT_TOKEN_TIME_OUT_IN_MINUTES = os.getenv('JWT_TOKEN_TIME_OUT_IN_MINUTES')
    JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES = os.getenv('JWT_REFRESH_TOKEN_TIME_OUT_IN_MINUTES')
    


class DevelopmentConfig(Config):    
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:iphone21@localhost/hoi'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@127.0.0.1:5432/solution_makers'
    engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, poolclass=NullPool)
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@13.127.252.10:5000/fivefloors'
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ECHO = True
    DEVELOPMENT = True
    DEBUG = True
    FIXED_RATE = 200




# redis_client = 'clien conn goes here'
app_config = {
    'development': DevelopmentConfig,
    # 'production': ProductionConfig
}



