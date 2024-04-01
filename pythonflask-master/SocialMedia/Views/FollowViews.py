from factory import db
from SocialMedia.Model.Models import Follow,Users
from flask import Blueprint,request,jsonify
from SocialMedia.helper import ResponseBody,save,update,FollowerDetails,FollowingsDetails
from SocialMedia.Views.PostView import query_list_to_dict,Success
# from SocialMedia.Views.UserViews import token_required
followblue=Blueprint('followBlue',__name__,url_prefix="/follow") 


@followblue.route("/addFollow",methods=["POST"])
def addFollower():
    data=request.get_json()
    sender_id=data.get('sender_id')
    receiver_id=data.get('receiver_id')
    get_AccountType=Users.query.filter_by(id=receiver_id).first()
    get_users=Follow.query.filter_by(receiver_id=receiver_id,sender_id=sender_id).first()
    if get_users:
         return jsonify({"Message":"Already Requested"}),400
    if get_AccountType.account_type == "private":
           follow=Follow(sender_id=sender_id,receiver_id=receiver_id)
           save(follow)
    else:
            follow=Follow(sender_id=sender_id,receiver_id=receiver_id,status=True)
            receiver=Users.query.filter_by(id=receiver_id).first()
            receiver.followers+=1
            update()
            sender=Users.query.filter_by(id=sender_id).first()
            sender.following+=1
            update()
            save(follow)
    return ResponseBody("Follow details saved successfully"),200


@followblue.route("/UpdateFollow",methods=["PUT"])
def UpdateFollow(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
     return jsonify({"Message":"Can't perform Task"}),401
   data=request.get_json()
   getFollow=Follow.query.filter_by(sender_id=data.get('sender_id'),receiver_id=data.get('receiver_id')).first()
   print(getFollow.status,"status")
   getFollow.status=True
   update()
   sender=Users.query.filter_by(id=data.get('sender_id')).first()
   sender.following+=1
   update()
   receiver=Users.query.filter_by(id=data.get('receiver_id')).first()
   receiver.followers+=1
   update()
   return ResponseBody("Follow Details Updated succcessfully")



@followblue.route("/getFollowers", methods=["GET"])
def getfollowersofuser():
#     if currentuser.Email!='buvanesh1902@gmail.com':
#      return jsonify({"Message":"Can't perform Task"}),401
    user_id = request.args.get('id')
    followers = Follow.query.filter_by(receiver_id=user_id).all()
    if followers:
          return FollowerDetails(followers=followers,user_id=user_id),200
    else :
         return ResponseBody("No Followers Found"),400



@followblue.route("/getFollowings",methods=["GET"])
def getfolloweringofuser():
     user_id=request.args.get('id')
     followings=Follow.query.filter_by(sender_id=user_id).all()
     if followings:
          return FollowingsDetails(followings=followings)
     else:
          return ResponseBody("No Followings Found"),400
          