# app/__init__.py
from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import *


db = SQLAlchemy()
BASE_URL_PREFIX = ''    
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    config_name = 'development'
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False 
    ''' App initialisation '''
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    # Enabling CORS
    CORS(app)
    return app



def register_blueprints(app):
 
    from SocialMedia.Views.UserViews import blu
    from SocialMedia.Views.FollowViews import followblue
    from SocialMedia.Views.PostView import Postblue
    from SocialMedia.Views.LikeViews import LikeBlue
    if BASE_URL_PREFIX:
        # app.register_blueprint(blue, url_prefix=BASE_URL_PREFIX)
       
        app.register_blueprint(blu,url_prefix=BASE_URL_PREFIX) 
        app.register_blueprint(followblue, url_prefix=BASE_URL_PREFIX)
        app.register_blueprint(Postblue, url_prefix=BASE_URL_PREFIX)
    else:
        # app.register_blueprint(blue)
        
        app.register_blueprint(blu)
        app.register_blueprint(followblue)
        app.register_blueprint(Postblue)
        app.register_blueprint(LikeBlue)
