import re
import sqlite3
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