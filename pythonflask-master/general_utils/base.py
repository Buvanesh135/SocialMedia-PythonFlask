import enum
from . api_error import ServerError
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import text, inspect, DateTime, String, Boolean, Column, Enum
from flask_sqlalchemy import SQLAlchemy
from flask import g
import uuid
import traceback
db = SQLAlchemy()
base = declarative_base()

class Status(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPEND = "SUSPEND"

def default_uuid():
    return uuid.uuid4().hex


class Base(db.Model):
    __abstract__ = True  # d m a v  
    id = Column(String(40), primary_key=True, default=lambda: default_uuid())
    created_on = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow,
                        server_default=text('NOW()'))
    updated_on = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow,
                        onupdate=datetime.utcnow, server_default=text('NOW()'))
    deleted_on = Column(DateTime(timezone=True), server_default=None)
    created_by = Column(String(50), server_default="")
    deleted_by = Column(String(50), server_default="")
    updated_by = Column(String(50), server_default="")
    is_deleted = Column(Boolean, default=False, server_default=text('FALSE'))

    def serialize(self) :
        """ return a json-serializable version of the object """
        return {c : getattr(self, c) for c in self.__serialize_attributes__}

    def to_dict(self) :
        """ return all attributes as json object """
        return {c : getattr(self, c) for c in inspect(self).attrs.keys()}

    def commit() :
        try :
            db.session.commit()
        except Exception as e :
            db.session.rollback()
            raise ServerError(str(e))
    def flush() :
        try :
            db.session.flush()
        except Exception as e :
            db.session.rollback()
            raise ServerError(str(e))

    def add(self) :
        user_id = getattr(g, "user_id", "")
        self.created_by = user_id
        db.session.add(self)
        self.commit()

    def delete(self) :
        user_id = getattr(g, "user_id", "")
        self.deleted_by = user_id
        self.is_deleted = True
        db.session.delete(self)
        self.commit()

    def soft_delete(self) :
        user_id = getattr(g, "user_id", "")
        self.status = "INACTIVE"
        self.deleted_by = user_id
        self.deleted_on = datetime.now()
        self.is_deleted = True
        self.commit()


    def update(self, attributes=None) :
        """ update object with attributes list """
        user_id = getattr(g, "user_id", "")
        self.updated_by = user_id
        self.commit()


    def update_with_list(self) :
        for val in self :
            val.update()


    def save_without_commit(self) :
        user_id = getattr(g, "user_id", "")
        self.created_by = user_id
        db.session.add(self)
        self.flush()


    def update_without_commit(self, attributes) :
        user_id = getattr(g, "user_id", "")
        self.updated_by = user_id
        for key, value in attributes.items() :
            setattr(self, key, value)
        self.flush()


    def delete_without_commit(self) :
        user_id = getattr(g, "user_id", "")
        self.deleted_by = user_id
        self.is_deleted = True
        db.session.delete(self)
        self.flush()


def query(cls) :
    return db.session.query(text(cls)).filter_by(is_deleted=False)

# t v s a  an pr 
def raw_execute(sql):
    try:
        result = db.engine.execute(text(sql).execution_options(autocommit=True))
        return result
    except Exception :
        print(traceback.format_exc())


def raw_select(sql):
    try:
        result_proxy = raw_execute(sql)
        result = []
        for row in result_proxy:
            row_as_dict = dict(row)
            date_ = row_as_dict.values()
            result.append(row_as_dict)
        result_proxy.close()
        return result
    except Exception as err:
        # log.exception(traceback.print_exc())
        return []
