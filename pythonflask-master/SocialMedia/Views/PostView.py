from SocialMedia.Model.Models import Post,Follow
from flask_mail import Mail
from flask_mail import Message
from factory import create_app
from flask import request,jsonify,Blueprint
from SocialMedia.helper import save,ResponseBody,ResponseBodyAllPostData,ResponseBodySinglePostData,PostofFollowings
from general_utils.json_utils import query_list_to_dict,Success
Postblue=Blueprint('PostBlue',__name__,url_prefix="/post")


app=create_app(__name__)
mail=Mail()
@Postblue.route("/Addpost",methods=["POST"])
def Addpost():
    data=request.get_json()
    if 'name' in data and 'user_id' in data :
        post=Post(post_name=data.get('name'),user_id=data.get('user_id'),likes=0)
        save(post)
        return ResponseBody("Post Added successfully"),200
    else:
        return ResponseBody("Enter the Valid Post details"),400
    

@Postblue.route("/getPostofonefollower",methods=["GET"])
def getPostofonefollower():
   data=request.args.get('id')
   if data:
      post=Post.query.with_entities(Post.id,Post.post_name)



@Postblue.route("/GetPost",methods=["GET"])
def GetPost():
    getallPost=Post.query.with_entities(Post.post_name,Post.user_id).all()
    if getallPost:
      msg="this is title"
      sender="20p308@kce.ac.in"
      receiver="buvanesh1902@gmail.com"
      msg=Message(msg,sender=sender,recipients=[receiver])
      mail.init_app(app)
      mail.send(msg)
      return ResponseBodyAllPostData(getallPost),200
    else :
      return ResponseBody("No data Exist"),400


@Postblue.route("/GetSinglePost",methods=["GET"])
def GetSinglePost():
    payload=request.args.get('id')
    post=Post.query.filter_by(id=payload).first()
    if post:
      return ResponseBodySinglePostData(post),200
    else :
      return ResponseBody("No data Exist"),400



@Postblue.route("/GetallPostofUser",methods=["GET"])
def GetallPostofUser():
   payload=request.args.get('id')
   post=Post.query.filter(Post.user_id==payload).with_entities(Post.post_name,Post.likes,Post.user_id).order_by((Post.created_at.desc())).all()
   if post:
        result = query_list_to_dict(post)
        print(post,"  posters  ",result,"  result ")
        return Success(result,payload),200
   else:
       return ResponseBody("No Post Found of User"),400
   


@Postblue.route("/getPaginationofPost",methods=["GET"])
def getPaginationofPost():
   page_no=request.args.get('page_no',default=1,type=int)
   totalrecords=request.args.get('per_pages',default=3,type=int)
   post=Post.query.with_entities(Post.post_name,Post.id,Post.user_id).paginate(page=page_no,per_page=totalrecords)
   if post:
       result=query_list_to_dict(post)
       return Success(result,0),200


@Postblue.route("/GetPostOfFollowings",methods=["GET"])
def GetPostOfFollowings():
   user_id=request.args.get('id')
   Followings=Follow.query.filter_by(sender_id=user_id).all()
   if Followings:
      return PostofFollowings(Followings),200
   else:
      return ResponseBody("No followings Found"),400
         
