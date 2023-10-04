from flask import Blueprint, request, jsonify
from function_jwt import write_token, validar_token

routes_auth = Blueprint("test", __name__)

@routes_auth.route("/login", methods =["POST"])
def login():
    data = request.get_json()
    if data['username'] == "Barbara":
        return write_token(data)
    else:
        response = jsonify({"message": "User not Found"})
        response.status_code = 404
        return response

@routes_auth.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split("")[1]
    return validar_token(token, output= True)