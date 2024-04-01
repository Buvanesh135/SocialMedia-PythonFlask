""" Error handlers """
import os
import sys

from flask import request,jsonify

from . response import Responses as Response
from constants import common

# from flask_sqlalchemy_session import current_session as session
def get_error_code(error):
    error_code = getattr(error, 'error_code', None)
    if error_code:
        return error_code
    error_code = getattr(error, 'code', common['SERVER_ERROR'])
    if error_code:
        return error_code
    return common['SERVER_ERROR']

def get_err():
    pass

def get_error(err):
    if err=="Internal Server":
        return jsonify({"Message":err}),500
    elif err=="Bad Request":
        return jsonify({"Message":err}),400
    elif err=="Unauthorized Access":
        return jsonify({"Message":err}),401


def handle_error(error):
    """ Error handler """
    # session.rollback()
    description = ''
    if hasattr(error, 'description'):
        description = error.description
    if not description:
        description = ",\n ".join([str(x) for x in error.args])

    if hasattr(error, 'code'):
        status_code = error.code
    else:
        status_code = 400

    if hasattr(error, 'status'):
        status = error.status
    else:
        status = None

    if hasattr(error, 'data'):
        data = error.data
    else:
        data = None
    error_code = getattr(error, 'error_code', None)

    exc_type, exc_obj, exc_tb = sys.exc_info()
    filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    request_url = request.environ.get('werkzeug.request').url
    is_server_error = getattr(error, "server_error", True)
    if is_server_error:
        # try:
        #     if request.method == "POST":
        #         request_body = str(request.json) if request.data else ""
        #     else:
        #         request_body = ""
        # except Exception as e:
        #     request_body = ""
        try:
            request_body = str(request.json) if request.data else ""
        except Exception as e:
            request_body = ""
        """log_exception(request_url, request.method, description, filename, "",
                      traceback.format_exc(), request_body)"""
        return Response.failure(code=status_code, error_code=error_code,
                                alert_msg_description=description,
                                alert_msg_type=common["FAILURE_ALERT"],
                                status=status, result=data)
    else:
        return Response.failure(code=status_code, error_code=error_code,
                                alert_msg_description=description,
                                alert_msg_type=common["FAILURE_ALERT"],
                                status=status, result=data,
                                is_access_log_required=True)
