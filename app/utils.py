from .db_queries import db_get_one

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