from flask import request, g, Response, Blueprint
from config import Config
from constants import common
from flask import redirect
from .logging import log_data
from .response import Responses as responses
from datetime import datetime
from .api_call import make_api_call
from Whitelisted import WHITELISTED
from SocialMedia.helper import failure
from connection import raw_select_read_replica
import jwt
def applicationBeforeRequest():
    """
    MiddleWare
    """
    accessToken = request.environ.get("HTTP_AUTHORIZATION",None)
    requestPath = request.environ.get("PATH_INFO")
    requestMethod = request.environ.get("REQUEST_METHOD")
    if requestMethod =="OPTIONS":
        return
    if requestPath == "/" or requestPath == "":
        return
    overallPath = requestPath.split('/')[-1]
    subPath = requestPath.split('/')[-2]
    if not (overallPath in WHITELISTED or subPath in WHITELISTED):
        if accessToken:
            isTokenValid,isUserValid, tokenExpired = validateTokens(accessToken)
            if not(isTokenValid and isUserValid) and not tokenExpired: 
                return failure("Invalid Token",status_code=401)
            if tokenExpired:
                return failure("Token Expired", status_code=403)
        else:
            return failure("Token Missing", status_code=403)
        

def validateTokens(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
            # print(payload)
            is_authorised = authenticatedUser(payload['identity'])
            return True, is_authorised , False
        except Exception as err:
            # print("unauth user falling here")
            return False, None, True
        

def authenticatedUser(user_id):
    if 'TEMP' in  user_id:
        validate_query = f"select id from temp_user where user_id='{user_id}'"
        return True if raw_select_read_replica(validate_query) else False
    elif user_id.startswith('CMS'):
            user_id = user_id[4:]
            user_query = f"select id from admin_users where id= '{user_id}'"
            return True if raw_select_read_replica(user_query) else False
    validate_query = f"select id from user_data where id='{user_id}'"
    return True if raw_select_read_replica(validate_query) else False



def after_check(response):
    if request.method == "OPTIONS":
        return Response()
    response_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    logging_enable = int(Config.LOG_ENABLE) if Config.LOG_ENABLE else 0
    if logging_enable:
        log_data(request, response, g.request_time, response_time)
    response.headers['Server'] = 'Application Server'
    response.headers['Strict-Transport-Security'] = 'max-age=16070400 ; includeSubDomains'
    response.headers['X-Frame-Options'] = 'deny'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = 'script-src "self"'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers[
        'Feature-Policy'] = "vibrate 'none'; geolocation 'none'; midi 'none'; notifications 'none'; push 'none'; sync-xhr 'none'; camera 'none'; microphone 'none'; speaker 'none'; magnetometer 'none'; gyroscope 'none'; fullscreen 'none'; payment 'none'"
    response.headers['Cache-Control'] = 'private, no-cache, no-store, max-age=0, no-transform'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0
    return response


ALIVE_SERVICE_BLUEPRINT = Blueprint('alive-service', __name__, url_prefix='/api/')


@ALIVE_SERVICE_BLUEPRINT.route('/is_alive', methods=["GET"])
def get_live_status():
    import json
    """
    This api is to get live status
    """
    resp = {
        "response": {
            "code": 200,
            "error_code": 0,
            "status": "success",
            "alert": [{
                "message": "api is alive",
                "type": "SUCCESS"
            }],
            "from_cache": 0,
            "is_data": 0
        }
    }
    return Response(json.dumps(resp), mimetype='text/json'), 200


def cache_access_token(key, value, expire=False):
    import json
    from config import redis_client
    if expire:
        redis_client.set(key, json.dumps(value), ex=value['access_token_expiry'])
    else:
        redis_client.set(key, value)


def validate_internal_api(token):
    from config import redis_client
    import json
    app_token = redis_client.get(Config.APPLICATION_ID)
    print(app_token, "app_token_cache")
    if app_token:
        return True
    else:
        authenticate_url = Config.AUTHENTICATION_BASE_URL + '/api/v1/authenticate/micro_service'
        auth_payload = {"application_id": str(Config.APPLICATION_ID)}
        auth_code, auth_resp = make_api_call(method_type='POST', url=authenticate_url, json=auth_payload,
                                             no_header=True,
                                             internal=True)
        if auth_code != 200:
            print("microservice authentication api failed")
            return False

        if auth_code == 200:
            json_resp = auth_resp.json()
            app_token = json_resp["data"]["access_token"]
            cache_access_token(Config.APPLICATION_ID, app_token)
            return True

