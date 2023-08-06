from app import app
from flask import request, jsonify
import datetime
import sqlite3
from flask_bcrypt import Bcrypt
from .validators import (
    validate_password_match,
    validate_password,
    validate_email,
    validate_unique_email,
    
)
from .db_queries import db_insert_one


@app.route("/admin", methods=["POST"])
def register_admin():
    data = request.get_json()

    # check if all required fields are present
    if data["email"] is None:
        message = {"error_message": "email is required"}
        return jsonify(message), 400
    if data["password"] is None:
        message = {"error_message": "password is required"}
        return jsonify(message), 400
    if data["password2"] is None:
        message = {"error_message": "password2 is required"}
        return jsonify(message), 400
    if data["first_name"] is None:
        message = {"error_message": "first name is required"}
        return jsonify(message), 400
    if data["last_name"] is None:
        message = {"error_message": "last name is required"}
        return jsonify(message), 400
    if data["address"] is None:
        message = {"error_message": "address is required"}
        return jsonify(message), 400
    if data["dob"] is None:
        message = {"error_message": "date of birth is required"}
        return jsonify(message), 400
    if data["phone"] is None:
        message = {"error_message": "phone is required"}
        return jsonify(message), 400
    if data["gender"] is None:
        message = {"error_message": "gender is required"}
        return jsonify(message), 400

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
        return "done"
    else:
        return jsonify({"error_message": "something went wrong"}), 500