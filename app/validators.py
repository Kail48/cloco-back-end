import sqlite3,pathlib,re
from .db_queries import db_get_one

def validate_password_match(password1,password2):
    return password1==password2

#the following fucntion validate a password to be at least 8 characters long,
#contains at least a digit, uppercase and lowercase character
def validate_password(password):  
    if len(password) < 8:  
        return False  
    if not re.search("[a-z]", password):  
        return False  
    if not re.search("[A-Z]", password):  
        return False  
    if not re.search("[0-9]", password):  
        return False  
    return True  

def validate_email(email):
    regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")  
    print(re.fullmatch(regex,email))
    if re.fullmatch(regex,email):
        return True
    else:
        return False
#this function checks if the email used by user already exists in db
def validate_unique_email(email):
    query="SELECT * FROM user WHERE email=?"
    param=(email,)
    user=db_get_one(query=query,param=param)
    
    if user is not None:
        return False
    else:
        return True
#return true if all data present else return error message
def has_all_user_data(data):
    if "email" not in data:
        return "email is required"

    if "password" not in data:
        return "password is required"

    if "password2" not in data:
        return "password2 is required"

    if "first_name" not in data:
        return "first name is required"

    if "last_name" not in data:
        return "last name is required"

    if "address" not in data:
        return "address is required"

    if "dob" not in data:
        return "date of birth is required"

    if "phone" not in data:
        return "phone is required"

    if "gender" not in data:
        return "gender is required"
    return True
#returns a dict containing result of validation and message to show if validation failed
def has_all_artist_data(data):
    if "name" not in data:
        return {"result":False,"error_message": "email is required"}

    if "address" not in data:
        return {"result":False,"error_message": "address is required"}
    if "dob" not in data:
        return {"result":False,"error_message": "date of birth is required"}
    if "first_release_year" not in data.keys():
        return {"result":False,"error_message": "first_release_year is required"}
    if "gender" not in data:
        return {"result":False,"error_message": "gender is required"}
    return {"result":True}

def file_is_csv(file):
    file_extension = pathlib.Path(file.filename).suffix
    print("extension is ",file_extension)
    if file_extension==".csv":
        return True
    else:
        return False
#takes in string and returns false if it is not a year
def is_year(data):
    if len(data)!=4:
        return False
    #all year strings can be converted to int
    try:
        int(data)
    except:
        return False
    #reject float values
    if "." in data:
        return False
    return True

        