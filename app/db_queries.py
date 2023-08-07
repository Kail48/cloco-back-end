import sqlite3,json,math,datetime
from app import Database

# this function executes a single INSERT query, returns true if the process is successful
def db_insert_one(query, insert_data):
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()

        cur.execute(query, insert_data)
        print(cur.lastrowid)
        connection.commit()
        cur.close()

    except sqlite3.Error as error:
        print(error)
        return False
    finally:
        if connection:
            connection.close()
    return True


def db_get_one(query, param):
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()

        result = cur.execute(query, param).fetchone()
        cur.close()

    except sqlite3.Error as error:
        return None
    finally:
        if connection:
            connection.close()
    return result


def db_update_one(query, param):
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()

        result = cur.execute(query, param)
        connection.commit()
        cur.close()

    except sqlite3.Error as error:
        return None
    finally:
        if connection:
            connection.close()
    return True


def db_delete_one(query, param):
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()
        print("working with database query:", query, " param: ", param)
        result = cur.execute(query, param)
        print(result)
        connection.commit()
        cur.close()

    except sqlite3.Error as error:
        return None
    finally:
        if connection:
            connection.close()
    return result

#returns users in respective page, note*:only non admin users are selected
def db_get_all_users(page):
    items_per_page = 5
    offset = (page - 1) * items_per_page
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()
        #calculate total pages using all the records and items per page
        query_total = "SELECT COUNT(*) FROM user"
        cur.execute(query_total)
        total_users = cur.fetchone()[0]
        total_pages = math.ceil(total_users / items_per_page)
        #get users with offset
        query = "SELECT id, first_name, last_name, email, phone, dob, gender, address, created_at, is_admin FROM user WHERE is_admin = 0 LIMIT ? OFFSET ?"
        cur.execute(query, (items_per_page, offset))
        #convert tuple data into dictionary of records
        columns = [col[0] for col in cur.description]
        print("columns ", columns)
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()

    except sqlite3.Error as error:

        return None
    finally:
        if connection:
            connection.close()
    return {"users":result,"total_pages":total_pages}

def db_get_artist(id):
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()

        cur.execute("SELECT * FROM artist WHERE id = ?",(id,))
        columns = [col[0] for col in cur.description]
        artist=dict(zip(columns,cur.fetchone()))
        print(artist)
        cur.close()

    except sqlite3.Error as error:
        return None
    finally:
        if connection:
            connection.close()
    return artist

def insert_new_artist(data):
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """INSERT INTO artist(name,dob, gender, address, first_release_year,number_of_albums_released, created_at, updated_at)
    VALUES (?,?,?,?,?,?,?,?);"""
    insert_data = (
        data["name"],
        data["dob"],
        data["gender"],
        data["address"],
        data["first_release_year"],
        0,
        created_at,
        None,
    )
    print("sql")
    execute_query = db_insert_one(query=query, insert_data=insert_data)
    if execute_query:
        return True
    else:
        return False
    
#get artists per page
def db_get_all_artists_with_page(page):
    items_per_page = 5
    offset = (page - 1) * items_per_page
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()
        #calculate total pages using all the records and items per page
        query_total = "SELECT COUNT(*) FROM artist"
        cur.execute(query_total)
        total_artist = cur.fetchone()[0]
        total_pages = math.ceil(total_artist / items_per_page)
        #get users with offset
        query = "SELECT id, name,dob,first_release_year, number_of_albums_released, gender, address, created_at FROM artist LIMIT ? OFFSET ?"
        cur.execute(query, (items_per_page, offset))
        #convert tuple data into dictionary of records
        columns = [col[0] for col in cur.description]
        print("columns ", columns)
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()

    except sqlite3.Error as error:

        return None
    finally:
        if connection:
            connection.close()
    return {"artist":result,"total_pages":total_pages}

#get all artists from database as dictionary
def db_get_all_artists():
    try:
        connection = sqlite3.connect(Database.name)
        cur = connection.cursor()
        query = "SELECT id, name,dob,first_release_year, number_of_albums_released, gender, address, created_at FROM artist"
        cur.execute(query)
        #convert tuple data into dictionary of records
        columns = [col[0] for col in cur.description]
        print("columns ", columns)
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()

    except sqlite3.Error as error:

        return None
    finally:
        if connection:
            connection.close()
    return result
#takes in list of dictionary containing artist data
def insert_artist_bulk(artist_list):
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """INSERT INTO artist(name,dob, gender, address, first_release_year,number_of_albums_released, created_at, updated_at)
    VALUES (?,?,?,?,?,?,?,?);"""
    try:
        connection = sqlite3.connect(Database.name)
        cur = connection.cursor()
        for artist in artist_list:
            insert_data = (
            artist["name"],
            artist["dob"],
            artist["gender"],
            artist["address"],
            artist["first_release_year"],
            0,
            created_at,
            None,
            )
            cur.execute(query, insert_data)

        connection.commit()
                
    except sqlite3.Error as error:
            print(error)
            return False
    finally:
        if connection:
            connection.close()
    return True

def insert_new_music(data):
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = """INSERT INTO music(artist_id,title,album_name,genre,created_at, updated_at)
    VALUES (?,?,?,?,?,?);"""
    insert_data = (
        data["artist_id"],
        data["title"],
        data["album_name"],
        data["genre"],
        created_at,
        None,
    )
    print("sql")
    execute_query = db_insert_one(query=query, insert_data=insert_data)
    if execute_query:
        return True
    else:
        return False

def db_get_all_music_for_an_artist(artist_id):
    try:
        connection = sqlite3.connect(Database.name)
        cur = connection.cursor()
        query = "SELECT id, title,album_name,genre created_at FROM music WHERE artist_id = ?"
        param=(artist_id,)
        cur.execute(query,param)
        #convert tuple data into dictionary of records
        columns = [col[0] for col in cur.description]
        print("columns ", columns)
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()

    except sqlite3.Error as error:

        return None
    finally:
        if connection:
            connection.close()
    return result