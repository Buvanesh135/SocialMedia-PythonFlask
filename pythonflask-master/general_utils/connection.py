from sqlalchemy import text

# from common.logger import log_error
from config import Config as config
from factory import db


def add_item(obj):
    try:
        db.session.add(obj)
        db.session.commit()
        return obj
    except Exception as err:
        # db.session.rollback()
        # log_error()
        # log_error()
        return None
    # finally:
    #     db.session.close()


def add_all(obj):
    try:
        db.session.add_all(obj)
        db.session.commit()
        return obj
    except Exception as ex:
        print("add_all", ex)
        return None


def get_item(*args):
    try:
        result = db.session.query(*args)
        return result
    except Exception as err:
        return None
    # finally:
    #     db.session.close()


def update_item(obj):
    try:
        db.session.commit()
        return obj
    except Exception as err:
        # db.session.rollback()
        # log_error()
        # log_error()
        return None
    # finally:
    #     db.session.close()


def delete_item(obj):
    try:
        db.session.delete(obj)
        db.session.commit()
        return obj
    except Exception as err:
        # log_error()
        # db.session.rollback()
        return None
    # finally:
    #     db.session.close()


def raw_select(sql):
    try:
        result_proxy = raw_execution(sql)
        result = []
        for row in result_proxy:
            row_as_dict = dict(row)
            result.append(row_as_dict)
        result_proxy.close()
        return result
    except Exception as err:
        # log_error()
        return []


def raw_execution(sql):
    try:
        result = db.engine.execute(text(sql).execution_options(autocommit=True))
        return result
    except Exception as err:
        # log_error()
        return []


def get_count(sql):
    try:
        result = db.engine.execute(sql)
        if result:
            one_row = result.fetchone()
            return one_row[0]
        return None
    except Exception as err:
        return None



def raw_execution_replica(sql):
    try:
        result = config.READ_REPLICA_ENGINE.execute(text(sql).execution_options(autocommit=True))
        return result
    except Exception as err:
        # print(traceback.print_exc())
        # log_error()
        return None


def raw_select_read_replica(sql):
    try:
        result_proxy = raw_execution_replica(sql)
        result = []
        for row in result_proxy:
            row_as_dict = dict(row)
            result.append(row_as_dict)
        result_proxy.close()
        return result
    except Exception as err:
        # log_error()
        return []
    
def execute_delete(statement):
    try:
        db.session.execute(statement)
        db.session.commit()
        return True
    except Exception as err :
        # log_error()
        return None