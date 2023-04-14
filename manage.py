import datetime
import hashlib
from flask import Flask, session, request, redirect, url_for, render_template, flash
from flask_socketio import emit, join_room,SocketIO
import os
import query
import base64
# import cloud
import string
import random

def filename_generator():
    prefix = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.sample(prefix, random.randrange(5, 20)))

app = Flask(__name__)
app.config.update({
    'DEBUG':True,
    'TEMPLATES_AUTO_RELOAD' :True,
    'SECRET_KEY': os.urandom(10)
})

# bucket_name = 'chatting'
room_name = 'chat room'

socketio = SocketIO()

socketio.init_app(app)
user_dict = {}
user_list = []

## Get user login status
def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        userName = 'please sign in'
    else:
        loggedIn = True
        sql = "SELECT name FROM users WHERE email = %s"
        params = [session['email']]
        userName = query.query(sql,params)

        session['user'] = userName[0][0]
    return (loggedIn, userName[0][0])

## Determine whether the account password matches
def is_valid(email, password):
    sql = 'SELECT email, password, name FROM users'
    data = query.query_no(sql)

    if data is not None:
        for row in data:
            if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
                return row[2]
    
    return False

def get_history(user = None):
    mess = []

    if user is None:
        sql = "SELECT messages.message, messages.created_at, users.name, users.avatar_url, messages.user_id, messages.receiver_id, messages.type \
                    FROM messages, users where messages.user_id = users.name"
    
        messages = query.query_no(sql)
  
    else:
        sql = "SELECT messages.message, messages.created_at, users.name, users.avatar_url, messages.user_id, messages.receiver_id, messages.type \
                FROM messages, users where (users.name = %s OR messages.receiver_id = %s) AND messages.user_id = users.name"
        
        params = [user, user]
        messages = query.query(sql, params)

    if messages is not None:
        for message in messages:
            if message[6] == "image" or message[6] == "video":
                mess.append((
                    message[0],
                    message[1],
                    message[2],
                    message[3],
                    message[4],
                    message[5],
                    message[6]
                ))
            else:
                mess.append((
                    base64.b64decode(message[0]).decode('utf-8'),
                    message[1],
                    message[2],
                    message[3],
                    message[4],
                    message[5],
                    message[6]
                ))

    return mess

# Get time now
def get_now():
    now = datetime.datetime.now()
    now = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')

    return now

# Get user avatar by email
def get_avatar(email):
    sql = "SELECT avatar_url FROM users WHERE email = %s"
    params = [email]
    avatar_url = query.query(sql, params)

    return avatar_url

## Register
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        if is_valid(email, password):
            flash('Account already exists, please sign in')
            return render_template("login.html")
        else:
            sql = 'INSERT INTO users (email, password, name) VALUES (%s, %s, %s)'
            params = [email,hashlib.md5(password.encode()).hexdigest(),name]

            msg = query.update(sql,params)

            if msg == 'Changed successfully':
                flash('registration success')
                return render_template("login.html")
            else:
                flash('registration failed')
                return render_template('register.html')
    else:
        return render_template('register.html')

## Login
@app.route("/", methods = ['POST', 'GET'])
@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_socket = request.environ.get('wsgi.websocket')
        
        if is_valid(email, password):
            if email in user_dict:
                flash('user exists')
                return render_template('login.html')

            user_dict[email] = user_socket
            session['username'] = is_valid(email, password)
            session['email'] = email
            user_list.append(session['username'])
            
            flash('login successful')
            return redirect(url_for('index'))
        else:
            error = 'Invalid UserId / Password'
            flash('login failed')
            return render_template('login.html', error=error)
    else:
        # flash('login failed')
        return render_template('login.html')

## Logout
@app.route("/logout")
def logout():
    socketio.emit('status', {'join_user': session['username'], 'flag': False})
    
    user_dict.pop(session['email'])
    session.pop('email', None)
    session.pop('username', None)

    return redirect(url_for('login'))

## Index
@app.route("/index", methods = ['POST', 'GET'])
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        loggedIn, userName = getLoginDetails()

        avatar_url = get_avatar(session['email'])

        #get username
        sql = "SELECT name, avatar_url, email, id FROM users" 
        users = query.query_no(sql)

        return render_template("index.html",userName = userName,avatar_url=avatar_url[0][0],users = users)

## Chatroom
@app.route("/chatroom", methods = ['POST', 'GET'])
def chatroom():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        loggedIn, userName = getLoginDetails()

        mess = get_history(session['username'])

        sql = "SELECT name, avatar_url, id, email FROM users"
        users = query.query_no(sql)

        avatar_url = get_avatar(session['email'])

        return render_template("chatroom.html", userName = userName, message = mess, users = users, avatar_url = avatar_url, cur = user_list)

## History
@app.route("/history/<user>")
def profile(user):
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        # get user
        sql = "SELECT * FROM users WHERE name = %s"
        params = [user]
        data = query.query(sql, params)

        # get history by user
        mess = get_history(user)

        sql = "SELECT name from users"
        users = query.query_no(sql)

        charts = {}

        for us in users:
            if us[0] != user:
                charts[us[0]] = 0

        for message in mess:
            if message[2] == user:
                charts[message[5]] = int(charts[message[5]]) + 1
            elif message[5] == user:

                charts[message[2]] = int(charts[message[2]]) + 1

        return render_template('history.html', user = data[0], messages = mess, charts = charts, users = users)

## connect chat room
@socketio.on('connect', namespace='/chatroom')
def connect():
    print('connection succeeded')

## join the room
@socketio.on('joined', namespace='/chatroom')
def joined(information):
    # The 'joined' route is to pass in a room_name, assign a room to the websocket connection, and return a 'status' route
    room_name = 'chat room'
    user_name = session.get('user')

    avatar_url = get_avatar(session['email'])

    create_time = get_now()

    join_room(room_name)

    data = {
        'user_name': user_name,
        'text': 'Joined ' + user_name,
        'create_time': create_time,
        'avatar_url': avatar_url,
        'flag': True,
        'join_user': user_name
    }

    emit('status', data, room=room_name)

## receive chat messages
@socketio.on('text', namespace='/chatroom')
def text(information):
    text = information.get('text')

    # get username
    user_name = session.get('user')

    create_time = get_now()

    if information.get('receiver') is None:
        # Insert chat information into database, update database
        sql = 'INSERT INTO messages (message, user_id, created_at) VALUES (%s, %s, %s)'
        params = [base64.b64encode(text.encode('utf-8')), user_name, create_time]
    else:
        sql = 'INSERT INTO messages (message, user_id, created_at, receiver_id) VALUES (%s, %s, %s, %s)'
        params = [base64.b64encode(text.encode('utf-8')), user_name, create_time, information.get('receiver')]

    msg = query.update(sql, params)

    # Get user avatar
    avatar_url = get_avatar(session['email'])
    
    if information.get('receiver') is not None:
        data = {
            'user_name': user_name,
            'text': text,
            'create_time': create_time,
            'avatar_url': avatar_url,
            'receiver': information.get('receiver')
        }
    else:
        data = {
            'user_name': user_name,
            'text': text,
            'create_time': create_time,
            'avatar_url': avatar_url,
        }

    room_name = 'chat room'

    # Return the chat information to the front end
    
    emit('message', data, room=room_name)

# Connect Home
@socketio.on('Iconnect', namespace='/index')
def Iconnect():
    print('connection succeeded')

# The path to receive the replaced avatar
@socketio.on('avatar_url' ,namespace='/index')
def avatar_url(information):
    email = session['email']
    avatar_url = information.get('avatar_url')
    sql = "UPDATE users SET avatar_url = %s WHERE email = %s "
    params = [avatar_url,email]
    msg = query.update(sql, params)

    # get user id
    sql = "SELECT id FROM users WHERE email = %s"
    params = [session['email']]
    user_id = query.query(sql, params)  

    # Return the chat information to the front end
    emit('avatar_upload', {
        'avatar_url': avatar_url,
        'user_id': user_id[0][0]
    })

@socketio.on('file_upload', namespace='/chatroom')
def file_upload(information):
    user_name = session['username']
    file = information.get('file')
    file_type = information.get('type')

    create_time = get_now()

    if information.get('receiver') is None:
        # Insert chat information into database, update database
        sql = 'INSERT INTO messages (message, user_id, created_at, type) VALUES (%s, %s, %s, %s)'
        params = [file, user_name, create_time, file_type]
    else:
        sql = 'INSERT INTO messages (message, user_id, created_at, receiver_id, type) VALUES (%s, %s, %s, %s, %s)'
        params = [file, user_name, create_time, information.get('receiver'), file_type]

    msg = query.update(sql, params)

    if information.get('receiver') is not None:
        data = {
            'user_name': user_name,
            'text': file,
            'create_time': create_time,
            'avatar_url': get_avatar(session['email']),
            'receiver': information.get('receiver'),
            'file_type': file_type
        }
    else:
        data = {
            'user_name': user_name,
            'text': file,
            'create_time': create_time,
            'avatar_url': get_avatar(session['email']),
            'file_type': file_type
        }

    # Return the chat information to the front end
    
    emit('file_upload', data, room=room_name)

if __name__ == '__main__':
    socketio.run(app)