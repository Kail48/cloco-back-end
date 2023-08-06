import sqlite3
from app import Database
import json
import math
import datetime

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
        print("tp ",total_pages)
        #get users with offset
        query = "SELECT id, first_name, last_name, email, phone, dob, gender, address, created_at, is_admin FROM user WHERE is_admin = 0 LIMIT ? OFFSET ?"
        cur.execute(query, (items_per_page, offset))
        #convert tuple data into dictionary of records
        columns = [col[0] for col in cur.description]
        print("columns ", columns)
        result = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()

    except sqlite3.Error as error:
        print("error occured",error)
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
