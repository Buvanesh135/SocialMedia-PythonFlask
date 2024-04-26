import uuid
from sqlalchemy import inspect
from sqlalchemy import Column, DateTime, String, func
from factory import db

def default_uuid():
    return uuid.uuid4().hex


def serialize(self):
    return {c: getattr(self, c) for c in inspect(self).attrs.keys()}


class Base(db.Model):
    __abstract__ = True
    __mapper_args__ = {
        'confirm_deleted_rows': False  # this is for getting conformation while deleting row of mapped class
    }
    #  __mapper_args__ = {
    #     'polymorphic_on': type,          The __mapper_args__ attribute in SQLAlchemy is used to provide additional configuration options to the mapper when defining a mapped class for polymor inheritance
    #     'polymorphic_identity': 'node' 
    # } 
    
    id = Column(db.Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    update_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), default=None)
    created_by = Column(String(40), default=None)
    updated_by = Column(String(40), default=None)
    deleted_by = Column(String(40), default=None)
    status = Column(String(10), default=None)
   
    def _asdict(self):
        return serialize(self)


    def objects(*args):
        return db.session.query(*args)