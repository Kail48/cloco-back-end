from app import app
from flask import request, jsonify
import datetime
import sqlite3
from flask_bcrypt import Bcrypt
from .decorators import admin_required
from .validators import (
    validate_password_match,
    validate_password,
    validate_email,
    validate_unique_email,
    has_all_user_data,
    has_all_artist_data
)
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from .db_queries import db_insert_one, db_get_one, db_update_one,db_delete_one,db_get_all_users,db_get_artist,insert_new_artist


@app.route("/admin", methods=["POST"])
def register_admin():
    data = request.get_json()
    if has_all_user_data(data)!=True:
        return jsonify(error_message=has_all_user_data(data))
    # validate special form datas
    if validate_email(data["email"]) == False:
        message = {"error_message": "enter a valid email address"}
        return jsonify(message), 400
    if validate_unique_email(email=data["email"]) == False:
        message = {"error_message": "This email is already in use"}
        return jsonify(message), 400
    if validate_password(data["password"]) == False:
        message = {
            "error_message": "pasword must contain an uppercase letter, a digit and at least be 8 characters long"
        }
        return jsonify(message), 400
    if validate_password_match(data["password"], data["password2"]) == False:
        message = {"error_message": "passwords do not match"}
        return jsonify(message), 400
    bcrypt = Bcrypt(app)  # for password hashing
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """INSERT INTO user(first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at, is_admin)
    VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
    insert_data = (
        data["first_name"],
        data["last_name"],
        data["email"],
        hashed_password,
        data["phone"],
        data["dob"],
        data["gender"],
        data["address"],
        created_at,
        None,
        1,
    )
    execute_query = db_insert_one(query=query, insert_data=insert_data)
    if execute_query:
        return jsonify(message="successfully created admin user",email=data['email']),200
    else:
        return jsonify({"error_message": "something went wrong"}), 500
    
@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"error_message": "Credentials not provided"}), 400
    if "email" not in data:
        return jsonify({"error_message": "email not provided"}), 400
    if "password" not in data:
        return jsonify({"error_message": "password not provided"}), 400
    email = data["email"]
    password = data["password"]
    if validate_unique_email(email=email) == True:  # check whether email exists in db
        return jsonify({"error_message": "User with this email doesn't exist"}), 400
    query = "SELECT * FROM user WHERE email=?"
    param = (email,)
    user = db_get_one(query=query, param=param)
    if user is None:
        return jsonify({"error_message": "User with this email doesn't exist"}), 400
    bcrypt = Bcrypt(app)
    hashed_password_user = user[4]  # password is in 5th column of user table
    if bcrypt.check_password_hash(hashed_password_user, password) == False:
        return jsonify({"error_message": "Please enter correct credentials"}), 400
    access_token = create_access_token(identity=email)
    return jsonify(
        access_token=access_token, is_admin=True if user[5] == True else False
    )

# a protected route to verify if user is admin
@app.route("/admin/verify", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user_email = get_jwt_identity()
    
    query = "SELECT * FROM user WHERE email=?"
    param = (current_user_email,)
    user = db_get_one(query=query, param=param)
    if user is None:
        return jsonify(error_message="please login again"), 400
    return jsonify(is_admin=True if user[5] == True else False), 200

@app.route("/user", methods=["POST"])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json()
    # check if all required fields are present
    if has_all_user_data(data)!=True:
        return jsonify(error_message=has_all_user_data(data))
    # validate special form datas
    if validate_email(data["email"]) == False:
        message = {"error_message": "enter a valid email address"}
        return jsonify(message), 400
    if validate_unique_email(email=data["email"]) == False:
        message = {"error_message": "This email is already in use"}
        return jsonify(message), 400
    if validate_password(data["password"]) == False:
        message = {
            "error_message": "pasword must contain an uppercase letter, a digit and at least be 8 characters long"
        }
        return jsonify(message), 400
    if validate_password_match(data["password"], data["password2"]) == False:
        message = {"error_message": "passwords do not match"}
        return jsonify(message), 400
    bcrypt = Bcrypt(app)  # for password hashing
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """INSERT INTO user(first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at, is_admin)
    VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
    insert_data = (
        data["first_name"],
        data["last_name"],
        data["email"],
        hashed_password,
        data["phone"],
        data["dob"],
        data["gender"],
        data["address"],
        created_at,
        None,
        0,
    )
    execute_query = db_insert_one(query=query, insert_data=insert_data)
    if execute_query:
        return jsonify(message="successfully created new user",email=data['email']),200
    else:
        return jsonify({"error_message": "something went wrong"}), 500
    
@app.route("/user/<id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(id):
    if request.get_json() is None:
        return jsonify(error_message="Please provide data to update"),400
    #check if user with given id exists
    query = "SELECT * FROM user WHERE id=?"
    param = (id,)
    user = db_get_one(query=query, param=param)
    if user is None:
        return jsonify(error_message="The user with provided id doesn't exist")
    data=request.get_json()
    for key in data:
        
        query = f"UPDATE user SET {key} = ? WHERE id = ? "
        param=(data[key],id)
        if db_update_one(query=query,param=param)==False:
            return jsonify(error_message="something wrong"),400
    updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"UPDATE user SET updated_at = ? WHERE id = ? "
    param=(updated_at,id)
    if db_update_one(query=query,param=param)==False:
            return jsonify(error_message="something wrong"),400
    return jsonify(message="successfully updated",id=id),200

@app.route("/user/<id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(id):
    #check if user with given id exists
    query = "SELECT * FROM user WHERE id=?"
    param = (id,)
    user = db_get_one(query=query, param=param)
    if user is None:
        return jsonify(error_message="The user with provided id doesn't exist")
    query = f"DELETE FROM user WHERE id = ? "
    param=(id,)
    if db_delete_one(query=query,param=param)==False:
        return jsonify(error_message="something wrong"),400
    
    return jsonify(message="successfully deleted",id=id),200
@app.route("/users")
@jwt_required()
@admin_required
def get_users():
    page = request.args.get('page', default=1, type=int)
    #check if user with given id exists
    result=db_get_all_users(page=page)
    if result is None:
        return jsonify(error_message="database error"),500
    return jsonify(result),200

@app.route("/artist", methods=["POST"])
@jwt_required()
@admin_required
def create_artist():
    data = request.get_json()
    print("here")
    # check if all required fields are present
    if has_all_artist_data(data)["result"]==False:
        return jsonify(has_all_artist_data(data)["error_message"])
    if insert_new_artist(data)==True:
        return jsonify(message="created new artist"),200
    else:
        return jsonify(error_message="something went wrong"),500