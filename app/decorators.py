from functools import wraps
from flask import request,jsonify
from .db_queries import db_get_one
from flask_jwt_extended import get_jwt_identity
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_email = get_jwt_identity()
        query = "SELECT * FROM user WHERE email=?"
        param = (current_user_email,)
        user = db_get_one(query=query, param=param)
        if user is None:
            return jsonify(error_message="please login again")
        if user[5] == False:  # check if the user is admin
            return jsonify(error_message="admin privilege required"), 401
        return f(*args, **kwargs)
    return decorated_function