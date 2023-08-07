from flask import Flask 
from flask_jwt_extended import JWTManager
from datetime import timedelta


UPLOAD_FOLDER = '/home/kuroashi/cloco/cloco-back-end/app/uploaded_files' #path to save uploaded files
ALLOWED_EXTENSIONS = {'.csv'}
app=Flask(__name__)
app.config["JWT_SECRET_KEY"] = "cloco-code"  #I have used simple secret key and directly instead of fetching from env variable
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
jwt = JWTManager(app)
class Database:
    name="cloco_db"
#place import statements for modules within this packege to avoid circular import
from app import views