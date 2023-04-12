import sqlite3

## database query function
def query(sql,params):  
    # open database connection
    cursor = sqlite3.connect('chat.sqlite3', check_same_thread=False)
    
    try:
        result = cursor.execute(sql,params).fetchall()
        return result                                                       # return query result
    
    except:
        cursor.rollback()                                                   # rollback on error

    cursor.close()


## Database query function, without parameters
def query_no(sql):  
    # open database connection
    cursor = sqlite3.connect('chat.sqlite3', check_same_thread=False)

    try:
        result = cursor.execute(sql).fetchall()
        return result                                                       # return query result
    
    except:
        cursor.rollback()                                                   # rollback on error

    cursor.close()


## database query function for INSERT, UPDATE, DELETE
def update(sql,params):
    cursor = sqlite3.connect('chat.sqlite3', check_same_thread=False)

    try:
        cursor.execute(sql,params)
        cursor.commit()                                                     # execute sql statement
        return "Changed successfully"
    
    except:
        cursor.rollback()                                                   # rollback on error

    cursor.close()