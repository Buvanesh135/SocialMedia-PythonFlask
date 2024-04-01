from flask import Blueprint,request,jsonify
from SocialMedia.Model.Models import like,Post
from factory import db
from SocialMedia.helper import ResponseBody,save,update,UserdetailsOfLikes,ResponseBodySinglePostData,ResponseBodyAllPostData
LikeBlue=Blueprint('LikeBlue',__name__,url_prefix="/like")


@LikeBlue.route("/addlike",methods=["POST"])
def addlike(currentuser):
    if currentuser.Email!='buvanesh1902@gmail.com':
     return jsonify({"Message":"Can't perform Task"}),401
    payload=request.get_json()
    getlike=like.query.filter_by(post_id=payload.get('post_id'),user_id=payload.get('user_id')).first()
    post=Post.query.filter_by(id=payload.get('post_id')).first()
    if not getlike:
        Like=like(user_id=payload.get('user_id'),post_id=payload.get('post_id'))
        post.likes+=1
        update()
        save(Like)
        return ResponseBody("Like saved Successfully"),200
    else:
        if post.likes!=0:
           post.likes-=1
        update()
        db.session.delete(getlike)
        db.session.commit()
        return ResponseBody('disLiked Successfully'),200
 


@LikeBlue.route("/GetLikeDetailsofPost",methods=["GET"])
def GetLikeDetailsofPost(currentuser):
    if currentuser.Email!='buvanesh1902@gmail.com':
        return jsonify({"Message":"Can't perform Task"}),401
    post_id=request.args.get('id')
    userdetails=like.query.filter_by(post_id=post_id).all()
    if userdetails:
        return UserdetailsOfLikes(userdetails),200
    else:
        return ResponseBody("NO user Found"),400
    

@LikeBlue.route("/getLikeCountofpost",methods=["GET"])
def getLikeCountofpost(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
     return jsonify({"Message":"Can't perform Task"}),401
   post_id=request.args.get('id')
   postcount=like.query.filter_by(post_id=post_id).all()
   if postcount:
       return jsonify({"like_count":len(postcount)}),200
   else:
       return ResponseBody("NO likes Found for POST"),400


@LikeBlue.route("/getPostOfMoreLikes",methods=["GET"])
def getPostOfMoreLikes(currentuser):
   if currentuser.Email!='buvanesh1902@gmail.com':
    return jsonify({"Message":"Can't perform Task"}),401
   post=Post.query.order_by(db.desc(Post.likes)).first()
   if Post:
       return ResponseBodySinglePostData(post),200
   else:
       return ResponseBody("No Post Found"),400
   
   

@LikeBlue.route("/getLikedPostsofUser",methods=["GET"])
def getLikedPostsofUser():
    user_id=request.args.get('user_id')
    Posts=like.query.filter_by(user_id=user_id).all()
    if Posts:
      return ResponseBodyAllPostData(Posts),200
    else:
        return ResponseBody("No Liked post's exist"),400
    




