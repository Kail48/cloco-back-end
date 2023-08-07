from .db_queries import db_get_one
import csv,os
from werkzeug.utils import secure_filename
from app import app
def user_exists(id):
    query = "SELECT * FROM user WHERE id=?"
    param = (id,)
    user = db_get_one(query=query, param=param)
    if user is None:
        return False
    return True
def artist_exists(id):
    query = "SELECT * FROM artist WHERE id=?"
    param = (id,)
    user = db_get_one(query=query, param=param)
    if user is None:
        return False
    return True
#receives a filestorage object and returns dictionary
def artist_csv_to_dictionary(file):
    filename = secure_filename(file.filename) #save the file with secure name
    filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    d = {}
    field_names=["name","dob","gender","address","first_release_year","number_of_albums_released"]
    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f)
        artist_list=[]
        for row in reader:
            artist_dictionary={}
            for field_name in field_names:
                artist_dictionary[field_name]=row[field_name]
            artist_list.append(artist_dictionary)
        print(artist_list)
    
    #delete the file from server after operation is complete
    os.remove(filepath)
    return d