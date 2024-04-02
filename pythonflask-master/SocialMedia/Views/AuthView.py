from flask import Blueprint,request,make_response,jsonify
import datetime
from config import *
from SocialMedia.Model.Models import Users
import jwt
authblue=Blueprint('authprint',__name__,url_prefix="/auth")


@authblue.route("/login",methods=['GET'])
def login():
   auth=request.authorization
   if not auth or not  auth.username or not auth.password:
      return make_response('could not verify',401, {'WWW-Authenticate':'Basic realm="Login required!"'})
   user =Users.query.filter_by(Email=auth.username).first()
   if not user:
       return make_response('could not verify',401, {'WWW-Authenticate':'Basic realm="Login required!"'})
   if auth.password!=user.password:
       return make_response('could not verify',401, {'WWW-Authenticate':'Basic realm="Login required!"'})
   accesstoken = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)},Config.SECRET_KEY)
   refreshtoken=jwt.encode({'id':user.id,'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)},Config.REFRESH_SECRET_KEY)
   print(accesstoken,'token generated',Config.SECRET_KEY,"secret_key")
   return jsonify({'accesstoken': accesstoken,'refreshtoken':refreshtoken})


@authblue.route("/refreshtoken", methods=['POST'])
def refresh_token():
    refresh_token = request.json.get('refresh_token')
    try:
        decoded = jwt.decode(refresh_token, Config.REFRESH_SECRET_KEY, algorithms=['HS256'])
        user_id = decoded['id']
        new_access_token = jwt.encode({'id': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, Config.SECRET_KEY)
        return jsonify({'access_token': new_access_token})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401
