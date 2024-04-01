from factory import db
from uuid import uuid4
from SocialMedia.Model.BaseModel import Base


class Users(Base):
    __tablename__='Users'
    name=db.Column(db.String(30),nullable=False)
    Email=db.Column(db.String(30),nullable=False,unique=True)
    password=db.Column(db.String(30),nullable=False)
    ph_no=db.Column(db.String(10),nullable=False,unique=True)
    following=db.Column(db.Integer,default=0)
    followers=db.Column(db.Integer,default=0)
    account_type=db.Column(db.String(),default='private')
    interest=db.Column(db.String(15))
    
    
class Follow(Base):
     __tablename__='Follow'
     id = db.Column(db.Integer, primary_key=True)
     status = db.Column(db.Boolean, nullable=False, default=False)
     sender_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
     receiver_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
     sender = db.relationship("Users", foreign_keys=[sender_id] )
     receiver = db.relationship("Users", foreign_keys=[receiver_id])


class Post(Base):
     __tablename__='post'
     post_name=db.Column(db.String(30),nullable=False)
     user_id=db.Column(db.Integer,db.ForeignKey('Users.id'))  
     likes=db.Column(db.Integer,nullable=False)
     user=db.relationship("Users",foreign_keys=[user_id])


class like(Base):
     __tablename__='like'
     user_id=db.Column(db.Integer,db.ForeignKey('Users.id'))
     post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
     user=db.relationship("Users",foreign_keys=[user_id])
     post=db.relationship("Post",foreign_keys=[post_id])



