# import json
# from datetime import datetime
# from json import JSONDecodeError
# from flask import g

# from . api_error import InvalidData
# from config import Config
# from .constants import common
# # from .pub_sub import queue_logging
# # from .mask_data import MASK_DATA
# #
# # LOG_BASE_URL = Config.LOG_BASE_URL


# def log_data(request, response, request_time, response_time, end_points=None,
#              response_data=None, response_header={}):
#     """
#         This function is to do logging
#     @param end_points: Dict
#     @param request: LocalProxy
#     @param response: Response
#     @param request_time: Datetime
#     @param response_time: Int
#     @param response_data
#     @param response_header
#     @return:
#     """
#     request_headers = dict(request.headers)
#     http_method = request.method
#     query_string = request.args
#     try:
#         request_data = str(request.json) if request.data else ""
#     except Exception as e:
#         request_data = ""
#     # if request.method == "POST":
#     #     request_data = str(request.json) if request.data else {}
#     request_url = request.environ.get('werkzeug.request').url
#     # if check_request_url(request_url, request.url_root, end_points):
#     if response or response_data:
#         code = 200
#         if not response_data:
#             try:
#                 response_data = json.loads(response.response[0].decode("utf-8"))
#                 code = response_data["response"]["code"]
#             except (JSONDecodeError, UnicodeDecodeError, TypeError):
#                 response_data = ""
#             response_header = dict(response.headers)
#         if type(code) is int:  # and 200 <= code < 300
#             log_access(request_data=request_data, response_data=response_data,
#                        request_url=request_url, request_time=request_time,
#                        response_time=response_time, response_header=response_header,
#                        request_headers=request_headers, http_method=http_method,
#                        query_string=query_string, log_type='API_Access', type="response")
#     else:
#         log_access(request_data=request_data, request_url=request_url,
#                    request_time=request_time, request_headers=request_headers,
#                    http_method=http_method, query_string=query_string,
#                    log_type='API_Access', type="request")


# def check_request_url(request_url, base_url, end_points):
#     """
#         This function is to check the request url
#     @param base_url: String
#     @param end_points: Dict
#     @param request_url: string
#     @return: Boolean
#     """
#     url_list = []
#     for val in end_points:
#         url_list.append(base_url + val)
#     if request_url in url_list:
#         return True
#     return False


# def get_log_url(log_type):
#     log_end_points = common['LOG_ENDPOINTS']
#     if log_type == "API_Access":
#         return LOG_BASE_URL + log_end_points["API_Access"]
#     elif log_type == "External_API_Access":
#         return LOG_BASE_URL + log_end_points["External_API_Access"]
#     elif log_type == "Exception":
#         return LOG_BASE_URL + log_end_points["Exception"]
#     elif log_type == "Developer_Debug":
#         return LOG_BASE_URL + log_end_points["Developer_Debug"]
#     elif log_type == "Custom":
#         return LOG_BASE_URL + log_end_points["Custom"]
#     raise InvalidData("Invalid Log Type")


# def log_exception(endpoint, http_method, exception, file, method, exception_stack,
#                   request_body=""):
#     # print("LOG EXCEPTION = ", exception)
#     data = {
#         "endpoint": endpoint,
#         "http_method": http_method,
#         "exception": exception,
#         "file": file,
#         "method": method,
#         "request_body": request_body,
#         "exception_stack": exception_stack,
#         "application_id": str(getattr(g, "application_id", None)),
#         "user_id": getattr(g, "user_id", None),
#         "application_name": Config.APPLICATION_NAME

#     }
#     # url = get_log_url("Exception")
#     try:
#         # code, resp = make_api_call(method_type="POST", url=url, data=data, internal=True)
#         # if code == 200:
#         log_to_elk(data, "Exception")
#         return "Success"
#         # return "Failed"
#     except Exception as e:
#         pass


# def log_access(request_data, request_url, request_time,
#                http_method, log_type, response_header=None,
#                request_headers=None, query_string=None, response_code=None,
#                type="response", response_data=None, response_time=None, mask=None, remove=None):
#     response_time_diff = None
#     try:
#         if response_time:
#             response_time_diff = datetime.strptime(response_time, "%Y-%m-%dT%H:%M:%S.%f") - \
#                                  datetime.strptime(request_time, "%Y-%m-%dT%H:%M:%S.%f")
#             response_time_diff = float(str(response_time_diff.seconds) + "." + str(response_time_diff.microseconds))
#     except Exception as e:
#         response_time_diff = None
#     data = {
#         "endpoint": request_url,
#         "request_header": request_headers,
#         "response_header": response_header,
#         "http_method": http_method,
#         "query_string": query_string,
#         "request_body": request_data,
#         "request_received_time": request_time,
#         "response_sent_time": response_time,
#         "response_body": response_data,
#         "response_time": response_time_diff,
#         "log_type": log_type,
#         "type": type,
#         "application_id": str(getattr(g, "application_id", None)),
#         "user_id": getattr(g, "user_id", None),
#         "application_name": Config.APPLICATION_NAME
#     }
#     if response_code is not None:
#         data["response_code"] = response_code
#     try:
#         log_to_elk(data, log_type)
#         return "Success"
#     except Exception as e:
#         print(e)


# def log_to_elk(payload, log_type):
#     """ This method is to log data to elk """
#     payload["log_type"] = log_type
#     data = {"application_id": str(getattr(g, "application_id", "")), "user_id": payload.get("user_id", ""),
#             "application_name": getattr(g, "application_name", "")}
#     payload["data"] = data
#     from . aws_sqs import send_queue_message
#     send_queue_message(Config.SAVE_LOG_SQS, payload)


