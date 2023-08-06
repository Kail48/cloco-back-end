import sqlite3


# this function executes a single INSERT query, returns true if the process is successful
def db_insert_one(query, insert_data):
    try:
        connection = sqlite3.connect("test_database")

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
    user=None
    try:
        connection = sqlite3.connect("test_database")

        cur = connection.cursor()

        result=cur.execute(query, param).fetchone()
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
        connection = sqlite3.connect("test_database")

        cur = connection.cursor()

        result=cur.execute(query, param)
        connection.commit()
        cur.close()

    except sqlite3.Error as error:
        return None
    finally:
        if connection:
            connection.close()
    return True