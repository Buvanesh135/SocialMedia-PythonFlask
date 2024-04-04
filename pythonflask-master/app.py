import os
from factory import create_app, register_blueprints
from flask import request, g, Response, Blueprint,jsonify
from SocialMedia.Model.Models import Users
from authlib.integrations.flask_client import OAuth
from config import Config
from flask import redirect
from general_utils.Whitelisted import WHITELISTED
from SocialMedia.helper import failure
from general_utils.connection import raw_select_read_replica
import jwt
mail,app = create_app(__name__)


oauth = OAuth(app)
google = oauth.register(
    name='google',
    consumer_key=os.getenv('GOOGLE_CLIENT_ID'),
    consumer_secret=os.getenv('GOOGLE_SCRECT_KEY'),
    client_kwargs={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


#       MiddleWare
@app.before_request
def applicationBeforeRequest():
    """
    MiddleWare
    """
    accessToken=""
    if 'x-access-token' in request.headers:
        accessToken = request.headers["x-access-token"]
    requestPath = request.environ.get("PATH_INFO")
    requestMethod = request.environ.get("REQUEST_METHOD")
    if requestMethod =="OPTIONS":
        return  
    if requestPath == "/" or requestPath == "":
        return
    subPath = requestPath.split('/')[-1]
    if not (subPath in WHITELISTED):
        if accessToken:
            result= validateTokens(accessToken)
            if  result!=1:
                if result=="Token has expired":
                   return jsonify({"message": "Token has expired"}), 401
                if result=="Invalid token":
                    return jsonify({"message": "Invalid token"}), 401
        else:
            return failure("Token Missing", status_code=403)
        

def validateTokens(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
            current_user = Users.query.filter_by(id=payload["id"]).first()
            if not current_user:
                return "User id Not Found",401
            return 1
        except jwt.ExpiredSignatureError:
            return "Token has expired"
        except jwt.InvalidTokenError:
            return "Invalid token"
        except Exception as e:
            return jsonify({"message": str(e)}), 401   
            

register_blueprints(app)  
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', os.getenv('PORT')))


# if __name__ == '__main__':
#     app.run(port=5000)