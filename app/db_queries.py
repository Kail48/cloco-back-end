import sqlite3
from app import Database
import json
import math


# this function executes a single INSERT query, returns true if the process is successful
def db_insert_one(query, insert_data):
    try:
        connection = sqlite3.connect(Database.name)

        cur = connection.cursor()

        cur.execute(query, insert_data)

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
        connection.commit()
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
        query = "SELECT * FROM user LIMIT ? OFFSET ?"
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
