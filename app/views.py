from app import app
from flask import request, jsonify
import datetime,csv,io
from flask_bcrypt import Bcrypt
from .decorators import admin_required
from .utils import user_exists, artist_exists,artist_csv_to_dictionary,music_exists
from .validators import (
    validate_password_match,
    validate_password,
    validate_email,
    validate_unique_email,
    has_all_user_data,
    has_all_artist_data,
    file_is_csv,
    has_all_music_data,
    is_valid_music_genre,
    is_valid_date,
    is_year,
    is_valid_gender_data
)
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from .db_queries import (
    db_insert_one,
    db_get_one,
    db_update_one,
    db_delete_one,
    db_get_all_users,
    db_get_artist,
    db_get_all_artists,
    insert_new_artist,
    db_get_all_artists_with_page,
    insert_artist_bulk,
    insert_new_music,
    db_get_all_music_for_an_artist
)


@app.route("/admin", methods=["POST"])
def register_admin():
    data = request.get_json()
    if has_all_user_data(data) != True:
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
    if is_valid_date(data["dob"])==False:
        message = {"error_message": "Date format not valid. valid date format is YYYY-MM-DD"}
        return jsonify(message), 400
    if is_valid_gender_data(data["gender"])==False:
        message = {"error_message": "Gender must value must be one of these: 'M','F','O'"}
        return jsonify(message), 400
    bcrypt = Bcrypt(app)  # for password hashing
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """INSERT INTO user(first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at, is_admin)
    VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
    insert_data = (
        data["first_name"],
        data["last_name"],
        data["email"].lower(),
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
        return (
            jsonify(message="successfully created admin user", email=data["email"]),
            200,
        )
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
    email = data["email"].lower()
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
    if has_all_user_data(data) != True:
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
    if is_valid_gender_data(data["gender"])==False:
        message = {"error_message": "Gender must value must be one of these: 'M','F','O'"}
        return jsonify(message), 400
    if is_valid_date(data["dob"])==False:
        message = {"error_message": "Date format not valid. valid date format is YYYY-MM-DD"}
    bcrypt = Bcrypt(app)  # for password hashing
    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """INSERT INTO user(first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at, is_admin)
    VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
    insert_data = (
        data["first_name"],
        data["last_name"],
        data["email"].lower(),
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
        return (
            jsonify(message="successfully created new user", email=data["email"].lower()),
            200,
        )
    else:
        return jsonify({"error_message": "something went wrong"}), 500


@app.route("/user/<id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(id):
    if request.get_json() is None:
        return jsonify(error_message="Please provide data to update"), 400
    # check if user with given id exists
    if user_exists(id) == False:
        return jsonify(error_message="The user with provided id doesn't exist"), 400
    
    data = request.get_json()
    if "dob" in data:
        if is_valid_date(data["dob"])==False:
            message = {"error_message": "Date format not valid. valid date format is YYYY-MM-DD"}
            return jsonify(message), 400
    if "gender" in data:
        if is_valid_gender_data(data["gender"])==False:
            message = {"error_message": "Gender must value must be one of these: 'M','F','O'"}
            return jsonify(message), 400
    for key in data:
        query = f"UPDATE user SET {key} = ? WHERE id = ? "
        param = (data[key], id)
        if db_update_one(query=query, param=param) == False:
            return jsonify(error_message="something wrong"), 400
    updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"UPDATE user SET updated_at = ? WHERE id = ? "
    param = (updated_at, id)
    if db_update_one(query=query, param=param) == False:
        return jsonify(error_message="something wrong"), 400
    return jsonify(message="successfully updated", id=id), 200


@app.route("/user/<id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_user(id):
    # check if user with given id exists
    if user_exists(id) == False:
        return jsonify(error_message="The user with provided id doesn't exist")
    query = f"DELETE FROM user WHERE id = ? "
    param = (id,)
    if db_delete_one(query=query, param=param) == False:
        return jsonify(error_message="something wrong"), 400

    return jsonify(message="successfully deleted", id=id), 200


@app.route("/users")
@jwt_required()
@admin_required
def get_users():
    page = request.args.get("page", default=1, type=int)
    # check if user with given id exists
    result = db_get_all_users(page=page)
    if result is None:
        return jsonify(error_message="database error"), 500
    return jsonify(result), 200


@app.route("/artist", methods=["POST"])
@jwt_required()
@admin_required
def create_artist():
    data = request.get_json()
    
    # check if all required fields are present
    if has_all_artist_data(data)["result"] == False:
        return jsonify(has_all_artist_data(data)["error_message"])
    if is_year(str(data["first_release_year"]))==False:
        return jsonify(message="first_release_year is not a valid year"), 400
    if is_valid_date(data["dob"])==False:
            message = {"error_message": "Date format not valid. valid date format is YYYY-MM-DD"}
            return jsonify(message), 400
    if is_valid_gender_data(data["gender"])==False:
        message = {"error_message": "Gender must value must be one of these: 'M','F','O'"}
        return jsonify(message), 400
    if insert_new_artist(data) == True:
        return jsonify(message="created new artist"), 200
    else:
        return jsonify(error_message="something went wrong"), 500


@app.route("/artist/<id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_artist(id):
    if request.get_json() is None:
        return jsonify(error_message="Please provide data to update"), 400
    # check if user with given id exists
    if artist_exists(id) == False:
        return jsonify(error_message="The artist with provided id doesn't exist"), 400

    data = request.get_json()
    if "dob" in data:
        if is_valid_date(data["dob"])==False:
            message = {"error_message": "Date format not valid. valid date format is YYYY-MM-DD"}
            return jsonify(message), 400
    if "first_release_year" in data:
         if is_year(str(data["first_release_year"]))==False:
            return jsonify(message="first_release_year is not a valid year"), 400
    if "gender" in data:
        if is_valid_gender_data(data["gender"])==False:
            message = {"error_message": "Gender must value must be one of these: 'M','F','O'"}
            return jsonify(message), 400
    for key in data:
        query = f"UPDATE artist SET {key} = ? WHERE id = ? "
        param = (data[key], id)
        if db_update_one(query=query, param=param) == False:
            return jsonify(error_message="something wrong"), 400
    updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"UPDATE artist SET updated_at = ? WHERE id = ? "
    param = (updated_at, id)
    if db_update_one(query=query, param=param) == False:
        return jsonify(error_message="something wrong"), 400
    return jsonify(message="successfully updated", id=id), 200


@app.route("/artist/<id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_artist(id):
    # check if user with given id exists
    if artist_exists(id) == False:
        return jsonify(error_message="The artist with provided id doesn't exist")
    query = f"DELETE FROM artist WHERE id = ? "
    param = (id,)
    if db_delete_one(query=query, param=param) == False:
        return jsonify(error_message="something wrong"), 400

    return jsonify(message="successfully deleted", id=id), 200


@app.route("/artists")
@jwt_required()
@admin_required
def get_artists():
    page = request.args.get("page", default=1, type=int)
    result = db_get_all_artists_with_page(page=page)
    if result is None:
        return jsonify(error_message="database error"), 500
    return jsonify(result), 200

@app.route("/artists/csv",methods=["GET","POST"])
@jwt_required()
@admin_required
def generate_artist_csv():
    if request.method=="GET":
        data = db_get_all_artists()
        if data is None:
            return jsonify(error_message="database error"), 500
        try:
            # Create an in-memory file object
            csv_output = io.StringIO()
            csv_writer = csv.DictWriter(csv_output, fieldnames=data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(data)
            
            # Get the CSV content from the in-memory file
            csv_content = csv_output.getvalue()
            
            # Close the in-memory file
            csv_output.close()
            
            # Create a response with CSV content
            response = app.response_class(
                response=csv_content,
                status=200,
                mimetype='text/csv'
            )
            
            # Set the filename for download
            response.headers.set('Content-Disposition', 'attachment', filename='artists.csv')
            
            return response

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    if request.method=="POST":
        #check if the file is present
        if 'file' not in request.files:
            return jsonify(error_message="No file Provided"), 400
        file = request.files['file']
        #check if the file is empty
        if file.filename == '':
            return jsonify(error_message="No file selected"), 400
        if file_is_csv(file)==False:
            return jsonify(error_message="only csv files are supported"), 400
        artist_list=artist_csv_to_dictionary(file)
        if artist_list is None: #returns false if csv has invalid data
            return jsonify(error_message="CSV file has unsanitized data"), 400
        db_execute=insert_artist_bulk(artist_list=artist_list)
        if db_execute==False:
            return jsonify(error_message="failed to save data"), 500
        return jsonify(message="successfully added artists")   
   
@app.route("/music", methods=["POST"])
@jwt_required()
@admin_required
def create_music():
    data = request.get_json()
    
    # check if all required fields are present
    if has_all_music_data(data)["result"] == False:
        return jsonify(has_all_artist_data(data)["error_message"])
    #check if artist provided is in the database
    if artist_exists(data["artist_id"])==False:
        return jsonify(error_message="the artist with given id doesn't exist"), 400
    #check if genre is valid
    if is_valid_music_genre(data["genre"])==False:
         return jsonify(error_message="The genre isnt accepted, please select from :'rnb', 'jazz', 'country', 'rock', 'classic'"), 400
    if insert_new_music(data) == True:
        return jsonify(message="created new music"), 200
    else:
        return jsonify(error_message="something went wrong"), 500

@app.route("/music/<id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_music(id):
    if request.get_json() is None:
        return jsonify(error_message="Please provide data to update"), 400
    # check if user with given id exists
    if music_exists(id) == False:
        return jsonify(error_message="The music with provided id doesn't exist"), 400

    data = request.get_json()
    if "genre" in data:
        if is_valid_music_genre(data["genre"])==False:
         return jsonify(error_message="The genre isnt accepted, please select from :'rnb', 'jazz', 'country', 'rock', 'classic'"), 400
   
    for key in data:
        query = f"UPDATE music SET {key} = ? WHERE id = ? "
        param = (data[key], id)
        if db_update_one(query=query, param=param) == False:
            return jsonify(error_message="something wrong"), 400
    updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"UPDATE music SET updated_at = ? WHERE id = ? "
    param = (updated_at, id)
    if db_update_one(query=query, param=param) == False:
        return jsonify(error_message="something wrong"), 400
    return jsonify(message="successfully updated music", id=id), 200

@app.route("/music/<id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_music(id):
    # check if music with given id exists
    if music_exists(id) == False:
        return jsonify(error_message="The music with provided id doesn't exist")
    query = f"DELETE FROM music WHERE id = ? "
    param = (id,)
    if db_delete_one(query=query, param=param) == False:
        return jsonify(error_message="something wrong"), 400

    return jsonify(message="successfully deleted", id=id), 200

@app.route("/musics")
@jwt_required()
@admin_required
def get_musics():
    if(request.args.get("artist_id",type=int)) is None:
        return jsonify(error_message="please provide artist id"), 400
    artist_id=request.args.get("artist_id",type=int)
    if artist_exists(artist_id)==False:
        return jsonify(error_message="The artist with provided id doesn't exist")
    result = db_get_all_music_for_an_artist(artist_id=artist_id)
    if result is None:
        return jsonify(error_message="database error"), 500
    return jsonify(result), 200