from factory import db
from flask import jsonify
from general_utils.json_utils import query_list_to_dict,Success
from SocialMedia.Model.Models import Users
from SocialMedia.Model.Models import Post,like,Follow
def ResponseBody(message):
    return jsonify({"Message":message})


def save(obj):
         db.session.add(obj)
         db.session.commit()


def update():
      db.session.commit()


def ResponseBodyofDeleteUser(id):
     user=Users.query.filter_by(id=id).first()
     if user:
          db.query.session.delete(user)
          update()


def ResponseBodyUserSingleData(data):
     user=Users.query.with_entities(Users.name,Users.interest,Users.ph_no,Users.followers,Users.following).filter_by(id=data).first()
     print(user)
     Users_details=[]
     Users_details.append(user)
     Result=query_list_to_dict(Users_details)
     return Success(Result,0)


def ResponseBodyAllUserData(users):
     Result=query_list_to_dict(users)
     return Success(Result,0)


def ResponseBodyAllPostData(posts):
    result=query_list_to_dict(posts)
    return Success(result,0)


def ResponseBodySinglePostData(data):
      post=[]
      print(data.user_id,"user_id")
      singlepost=Post.query.with_entities(Post.id,Users.name,Users.interest,Users.ph_no,Post.post_name,Post.likes).join(Users,data.user_id==Users.id).first()
      post.append(singlepost)
      details=query_list_to_dict(post)
      return Success(details,0)


def FollowerDetails(followers,user_id):
       follow_data=[]
       for follow in followers:
            followers=Follow.query.with_entities(Follow.sender_id,Users.name,Users.interest,Users.account_type,Users.followers,Users.following).join(Users, Follow.sender_id == Users.id).filter(Follow.sender_id==follow.sender_id).first()
            follow_data.append(followers)
       followers_details=query_list_to_dict(follow_data)
       return Success(followers_details,0)


def FollowingsDetails(followings):
     followings_details=[]
     for follow in followings:
          following=Follow.query.with_entities(Follow.receiver_id,Users.interest,Users.account_type,Users.name,Users.followers,Users.following).join(Users, Follow.receiver_id == Users.id).filter(Follow.receiver_id==follow.receiver_id).first()
          followings_details.append(following)
     FollowingsDetails=query_list_to_dict(followings_details)
     return Success(FollowingsDetails,0)


def UserdetailsOfLikes(userdetails):
     UserdetailsOfLikes=[]
     for user in userdetails:
          eachuser=like.query.with_entities(like.user_id,Users.name,Users.Email,Users.followers,Users.following,Users.interest,Users.ph_no).join(Users,like.user_id==Users.id).first()
          UserdetailsOfLikes.append(eachuser)
     result=query_list_to_dict(UserdetailsOfLikes)
     return Success(result,0)


def PostofFollowings(followings):
    followingspost = []
    for following in followings:    
        following_posts = []
        for post in Post.query.filter_by(user_id=following.sender.id).all():
            # Extract specific attributes from the Post object
            post_details = {
                "post_name": post.post_name,
                "post_likes": post.likes
            }
            following_posts.append(post_details)
            following_dict.get('')

        following_dict = {
            "user_id": following.receiver.id,
            "postdetails": following_posts
        }
        followingspost.append(following_dict)

    return jsonify(followingspost)


def postofSuggestion(interest):
     users=Users.query.filter_by(interest=interest,account_type='public').all()
     if users:
      Suggestions=[
            {
                  "user_name":user.name,
                  "account_type":user.account_type,
                  "ph_no":user.ph_no,
                  "followers":user.followers,
                  "followings":user.following
            }
            for user in users
      ]
      return jsonify(Suggestions),200
     else:
          return ResponseBody("No Users Found"),400


def failure(data,status_code):
     return data,status_code

     