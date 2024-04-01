from flask import jsonify

# basically  it takes every record of data as entry and convert it into dictionary format for easy json format
def query_list_to_dict(query_list):
    return [entry._asdict() for entry in query_list]


def Success(message, user_id):
    data = {'data': message, 'error': 0}
    if user_id!=0:
        data['user_id'] = user_id
        data["message"]="All data retrived Successfully"
    resp = jsonify(data)  
    resp.status_code = 200
    resp.content_type = "application/json"
    return resp
