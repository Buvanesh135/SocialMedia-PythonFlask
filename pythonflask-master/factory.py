# app/__init__.py
from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_mail import Mail
import warnings

# Suppress the warning
warnings.filterwarnings("ignore", message="urllib3 .* doesn't match a supported ")

db = SQLAlchemy()
mail=Mail()
BASE_URL_PREFIX = ''

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    config_name = 'development'
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False 
    ''' App initialisation '''
    db.init_app(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'palanisamy.buvanesh@divum.in'
    app.config['MAIL_PASSWORD'] = 'tnizekbidjgrmeec'    
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_SLT']=False
    migrate = Migrate(app, db, compare_type=True)
    # app.config['MAIL_']
    mail.init_app(app)
    # Enabling CORS
    CORS(app)
    return mail,app


def register_blueprints(app):
    from SocialMedia.Views.UserViews import blu
    from SocialMedia.Views.FollowViews import followblue
    from SocialMedia.Views.PostView import Postblue
    from SocialMedia.Views.LikeViews import LikeBlue
    from SocialMedia.Views.AuthView import authblue
    if BASE_URL_PREFIX:
        app.register_blueprint(blu,url_prefix=BASE_URL_PREFIX) 
        app.register_blueprint(followblue, url_prefix=BASE_URL_PREFIX)
        app.register_blueprint(Postblue, url_prefix=BASE_URL_PREFIX)
        app.register_blueprint(authblue, url_prefix=BASE_URL_PREFIX)

    else:
        # app.register_blueprint(blu)
        app.register_blueprint(blu) 
        app.register_blueprint(followblue)
        app.register_blueprint(Postblue)
        app.register_blueprint(LikeBlue)
        app.register_blueprint(authblue)
                