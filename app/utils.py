from .db_queries import db_get_one
from .validators import is_year,is_valid_date
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
    field_names=["name","dob","gender","address","first_release_year","number_of_albums_released"]
    with open(filepath, mode='r') as f:
        reader = csv.DictReader(f)
        artist_list=[]
        #check for invalid data
        for row in reader:
            artist_dictionary={}
            #check if any data field is empty
            for key in row.keys():
                if row[key] is None:
                    return None
            #check if the release year is valid
            if is_year(row["first_release_year"])==False:
                return None
            #check if the date is in valid date format
            if is_valid_date(row["dob"])==False:
                return None
            #create a dictioanry from field list and append to the artist list
            for field_name in field_names:
                artist_dictionary[field_name]=row[field_name]
            artist_list.append(artist_dictionary)   
       

        print(artist_list)
    
    #delete the file from server after operation is complete
    os.remove(filepath)
    return artist_list