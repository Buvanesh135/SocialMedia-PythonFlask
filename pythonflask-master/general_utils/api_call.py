import requests
from flask import g
from . api_error import ServerError

def get_headers(content_type:str, internal:bool):
    app_access_token = getattr(g, "access_token", None)
    if not app_access_token and internal:
        raise ServerError("Can't make internal api call")
    header = dict()
    if internal:    
        header["accesstoken"] = app_access_token
    if content_type == "json":
        header["Content-Type"] = "application/json"
    elif content_type == "xml":
        header["Content-Type"] = "application/xml"
    elif content_type == "x-www-form-urlencoded":
        header["Content-Type"] = "application/x-www-form-urlencoded"
    return header


def make_api_call(method_type, url, params=None, json=None, header=None, internal=False,
                  content_type="json", timeout=None, verify=True):
    if internal and not timeout:
        timeout = 20
    header = get_headers(content_type,internal) if not header else None
    try:
        if method_type == "POST":
            resp = requests.post(url=url, headers=header, data=json, timeout=timeout, verify=verify, params=params)
        elif method_type == "GET":
            resp = requests.get(url=url, headers=header,timeout=timeout, verify=verify, params=params)
        elif method_type == "PUT":
            resp = requests.put(url=url, headers=header, data=json, timeout=timeout, verify=verify)
        elif method_type == "DELETE":
            resp = requests.delete(url=url, headers=header, data=json, timeout=timeout, verify=verify)
        else:
            return "Invalid method type"
        code = resp.status_code 
        return code, resp
    except Exception as e:
        return 400, str(e)
