
from factory import db
from SocialMedia.Model.Models import Users
# from flask_jwt_extended import create_access_token,create_refresh_token
from flask import Blueprint,make_response,jsonify,request
from SocialMedia.helper import ResponseBody,save,ResponseBodyUserSingleData,ResponseBodyAllUserData,update,postofSuggestion
from general_utils.json_utils import query_list_to_dict,Success
import jwt
import os
# import datetime
import secrets
from config import *
from functools import wraps
blu=Blueprint('blueprintss',__name__,url_prefix="/user")
secret_key = secrets.token_hex(32)

@blu.route("/newuser",methods=["POST"])
def CreateNew_User():
    data=request.get_json()
    try:
        if 'name' in data and 'email' in data and 'password' in data and 'ph_no' in data and 'interest' in data:
         getUser=Users.query.filter_by(Email=data.get('email')).first()
         if not getUser:
            new_user=Users(name=data.get('name'),Email=data.get('email'),password=data.get('password'),ph_no=data.get('ph_no'),interest=data.get('interest') ,created_by=data.get('name'))
            save(new_user)
            return ResponseBody("New User Created Successfully"),200
         else:
            return ResponseBody("User Already Exist not valid Email"),400
        else:
           return ResponseBody("Missing detials Enter all details"),400
    except:
       return ResponseBody("Enter the valid details"),400



# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#             print(token, "token")
#         else:
#             return jsonify({"message": "Token is missing"}), 401
#         try:
#             print(secret_key, 'secret_key')
#             data = jwt.decode(token, secret_key,algorithms=['HS256'])
#             print(data['id'], "data")
#             current_user = Users.query.filter_by(id=data["id"]).first()
#             if current_user is None:
#                 raise Exception("User not found")
#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token has expired"}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token"}), 401
#         except Exception as e:
#             return jsonify({"message": str(e)}), 401
#         return f(current_user, *args, **kwargs)
    
#     return decorated


@blu.route("/updateUser",methods=["PUT"])
def updateUser(currentuser):
   if currentuser!='buvanesh1902@gmail.com':
      return jsonify({"Message":"Can't perform task"}),401
   data=request.get_json()
   getUser=Users.query.filter_by(data.get('email')).first()
   if not getUser:
      return ResponseBody("User Doesn't exist "),400
   else:
       if 'name' in data:
          getUser.name=data.get('name')
       if 'interest' in data:
          getUser.interest=data.get('interest')
       if 'ph_no' in data:
          getUser.ph_no=data.get('ph_no')
       if 'followers' in data:
          getUser.followers=data.get('followers')
       if 'followings' in data:
          getUser.following=data.get('followings')
       db.session.commit()
       return ResponseBody("User Details Updates Successfully"),200



@blu.route("/getSingleUser",methods=["GET"])
def getSingleUser(currentuser):
  if currentuser.Email!='buvanesh1902@gmail.com':
   return jsonify({"Message":"Can't perform Task"}),401
  data=request.args.get('id')
  if not data:
     return ResponseBody("User not Present Enter the valid user id"),400
  else:
     return ResponseBodyUserSingleData(data),200
  


@blu.route("/getAllUsers",methods=["GET"])
def getAllUsers(currentuser):

   if currentuser.Email!='buvanesh1902@gmail.com':
      return jsonify({"Message":"Can't perform Task"})

   getUsers=Users.query.all()
   if not getUsers:
      return ResponseBody("No data is Exist"),400
   else:
      result = query_list_to_dict(getUsers)
      return Success(result,0),200



@blu.route("/getInterest",methods=["GET"])
def getInterest(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
    return jsonify({"Message":"Can't perform Task"}),401
   payload=request.args.get('interest')
   getAllUsers=Users.query.filter_by(interest=payload).all()
   if getAllUsers:
      return ResponseBodyAllUserData(getAllUsers),200
   else:
      return ResponseBody("NO User Found with Interest"),400


@blu.route("/UpdateUser",methods=["PUT"])
def UpdateUser(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
      return jsonify({"Message":"Can't perform Task"}),401
   payload=request.get_json()
   getuser=Users.query.filter_by(id=payload.get('id')).first()
   if getuser:
         if 'name' in payload:
            getuser.name=payload.get('name')
         if 'interest' in payload:
            getuser.interest=payload.get('interest')
         if 'ph_no' in payload:
            getuser.ph_no=payload.get('ph_no')
         if 'account_type' in payload:
            getuser.account_type=payload.get('account_type')
         update()
         return ResponseBody("User Details Updated Successfully"),200
   return ResponseBody("No user Found Enter valid details"),400


@blu.route("/DeleteUser",methods=["GET"])
def DeleteUser():
   user_id=request.args.get("id")
   user=Users.query.filter(Users.id==user_id).first()



@blu.route("/GetUserofPrivateAccount",methods=["GET"])
def GetUserofPrivateAccount():
   users=Users.query.filter_by(account_type='private').all()
   if users:
      return ResponseBodyAllUserData(users=users),200
   else:
      return ResponseBody("No User found with private Account"),400



@blu.route("/UpdateManyUsers",methods=["PUT"])
def UpdateManyUsers(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
      return jsonify({"Message":"Can't perform Task"}),401
   payload=request.get_json()
   for data in payload:
      if 'email' in data:
         user=Users.query.filter(Users.Email==data.get('email'))
         if 'name' in data:
            user.name=data.get('name')
         if 'account_type' in data:
            user.account_type=data.get('account_type')
         if 'interest' in data:
            user.interest=data.get('interest')
         if 'ph_no' in data:
            user.ph_no=data.get('ph_no')
         print('user_ph',user.ph_no)
         update()
      else:
          return ResponseBody("Enter the email Id to Update User details"),400
   return ResponseBody("Users details updates Successfully"),200
   


@blu.route('/getUserDetailofSuggestion',methods=["GET"])
def getUserDetailofSuggestion(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
      return jsonify({"Message":"Can't perform Task"}),401
   interest=request.args.get('interest')
   return postofSuggestion(interest=interest)



@blu.route("/getUserOfMoreFollowers")
def getUserOfMoreFollowers(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
      return jsonify({"Message":"Can't perform Task"}),401
   user=Users.query.order_by(db.desc(Users.followers)).all()
   if user:
      return ResponseBodyAllUserData(user),200
   else:
      return ResponseBody("No Users Found"),400
   


@blu.route("/getUsersofMoreFollowersPagnation")
def getUsersofMoreFollowersPagnation(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
      return jsonify({"Message":"Can't perform Task"}),401
   page_no=request.args.get('page_no',default=1,type=int)
   per_pages=request.args.get('per_pages',default=3,type=int)
   users=Users.query.order_by(db.desc(Users.followers)).paginate(page=page_no,per_page=per_pages)
   if users:
      return ResponseBodyAllUserData(users=users),200
   else:
      return ResponseBody("No users Found"),400








