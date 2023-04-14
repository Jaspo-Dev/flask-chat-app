import sqlite3
import pymysql

## database query function
def query(sql,params):  
    # open database connection
    # db = pymysql.connect(
    #         host = '34.135.27.3', 
    #         user = 'chatuser', 
    #         password = 'chatuser', 
    #         db = 'chatroom'
    #     )

    db = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="chatroom"
    )
    
    cursor = db.cursor()
   
    try:
        cursor.execute(sql,params)
        result = cursor.fetchall()

        return result                                                       # return query result
    
    except:
        db.rollback()                                                   # rollback on error

    cursor.close()
    db.close()

## Database query function, without parameters
def query_no(sql):  
    # open database connection
    # db = pymysql.connect(
    #         host = '34.135.27.3', 
    #         user = 'chatuser', 
    #         password = 'chatuser', 
    #         db = 'chatroom'
    #     )

    db = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="chatroom"
    )
    
    cursor = db.cursor()

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        return result                                                       # return query result
    
    except:
        db.rollback()                                                   # rollback on error

    cursor.close()
    db.close()


## database query function for INSERT, UPDATE, DELETE
def update(sql,params):
    # open database connection
    # db = pymysql.connect(
    #         host = '34.135.27.3', 
    #         user = 'chatuser', 
    #         password = 'chatuser', 
    #         db = 'chatroom'
    #     )

    db = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        db="chatroom"
    )
    
    cursor = db.cursor()

    try:
        cursor.execute(sql,params)
        db.commit()                                                     # execute sql statement
        return "Changed successfully"
    
    except:
        db.rollback()                                                   # rollback on error

    cursor.close()
    db.close()