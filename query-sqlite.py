import sqlite3
import pymysql

## database query function
def query(sql,params):  
# open database connection
    # mysql
    # db = pymysql.connect('localhost', 'root', 'taskdb', 'chatroom', charset='utf8')
    db = pymysql.connect('localhost', 'root', '', 'chatroom', charset='utf8')
    cursor = db.cursor()
    
#sqlite
    # cursor = sqlite3.connect('chat.sqlite3', check_same_thread=False)
    
    try:
        result = cursor.execute(sql,params).fetchall()
        return result                                                       # return query result
    
    except:
        cursor.rollback()                                                   # rollback on error

    cursor.close()
    db.close()

## Database query function, without parameters
def query_no(sql):  
# open database connection
    # mysql
    db = pymysql.connect(
            host = 'localhost', 
            user = 'root', 
            password = '', 
            db = 'chatroom'
        )
    cursor = db.cursor()

# sqlite
    # cursor = sqlite3.connect('chat.sqlite3', check_same_thread=False)

    try:
        result = cursor.execute(sql).fetchall()
        return result                                                       # return query result
    
    except:
        cursor.rollback()                                                   # rollback on error

    cursor.close()
    db.close()


## database query function for INSERT, UPDATE, DELETE
def update(sql,params):
# mysql
    db = pymysql.connect('localhost', 'root', '', 'chatroom', charset='utf8')
    cursor = db.cursor()

#sqlite
    # cursor = sqlite3.connect('chat.sqlite3', check_same_thread=False)

    try:
        cursor.execute(sql,params)
        cursor.commit()                                                     # execute sql statement
        return "Changed successfully"
    
    except:
        cursor.rollback()                                                   # rollback on error

    cursor.close()
    db.close()