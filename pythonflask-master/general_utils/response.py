import os
from flask import Response
from datetime import datetime
from .constants import MESSAGES
from decimal import Decimal
from flask.json import JSONEncoder as FlaskJSONEncoder
import enum
import datetime

DEBUG_MODE = os.getenv('DEBUG_MODE', 0)


class JSONEncoder(FlaskJSONEncoder):
    """ Custom JSON encoder """

    def default(self, obj):  # pylint: disable=method-hidden,arguments-differ
        """ Encode an object to JSON """

        if isinstance(obj, datetime.datetime):
            return obj.isoformat(timespec='milliseconds')

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, enum.Enum):
            return obj.value

        return super(JSONEncoder, self).default(obj)


class Responses:
    @staticmethod
    def failure(code, alert_msg_description =None, alert_msg_type=None, from_cache=0, status=None, result=None, error_code=None,
                is_access_log_required=False):
        """This api is to return json serialized response in failure case"""
        is_data = 1 if result else 0
        description = alert_msg_description if int(DEBUG_MODE) == 1 else MESSAGES["FAILURE_MSG"]
        error_code = error_code if error_code else code
        resp = {
            "response": {
                "code": code,
                "error_code": error_code,
                "status": status if status else "failure",
                "alert": [{
                    "message": description,
                    "type": alert_msg_type,
                }],
                "from_cache": from_cache,
                "is_data": is_data
            }
        }
        if is_data:
            resp["data"] = result
        if is_access_log_required:
            response_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
            """log_data(request=request, response=None, request_time=g.request_time,
                     response_time=response_time, response_data=resp, response_header={})"""
        return Response(resp, mimetype='text/json'), code

    @staticmethod
    def success(code,  alert_msg_description =None, alert_msg_type=None,from_cache=0, result=None, status=None):
        """This api is to return json serialized response in success case"""
        is_data = 1 if result else 0
        description = alert_msg_description if int(DEBUG_MODE) == 1 else MESSAGES["SUCCESS_MSG"]
        resp = {
            "response": {
                "code": code,
                "error_code": 0,
                "status": status if status else "success",
                "alert": [{
                    "message": description,
                    "type": alert_msg_type
                }],
                "from_cache": from_cache,
                "is_data": is_data
            }
        }
        if is_data:
            resp["data"] = result
        # return Response(json.dumps(resp, cls=JSONEncoder), mimetype='text/json'), code
        return Response(resp, mimetype='text/json'), code
