import datetime
import hashlib
from flask import Flask, session, request, redirect, url_for, render_template, flash
from flask_socketio import emit, join_room,SocketIO
import os
import query

app = Flask(__name__)
app.config.update({
    'DEBUG':True,
    'TEMPLATES_AUTO_RELOAD' :True,
    'SECRET_KEY': os.urandom(10)
})

socketio = SocketIO()

socketio.init_app(app)
user_dict = {}

## Get user login status
def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        userName = 'please sign in'
    else:
        loggedIn = True
        sql = "SELECT name FROM users WHERE email = ?"
        params = [session['email']]
        userName = query.query(sql,params)

        session['user'] = userName[0][0]
    return (loggedIn, userName[0][0])

## Determine whether the account password matches
def is_valid(email, password):
    sql = 'SELECT email, password FROM users'
    data = query.query_no(sql)

    if data is not None:
        for row in data:
            if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
                return True
    
    return False

## Register
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Parse form data
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        if is_valid(email, password):
            flash('Account already exists, please log in')
            return render_template("login.html")
        else:
            sql = 'INSERT INTO users (email, password, name) VALUES (?, ?, ?)'
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
        user_dict[email] = user_socket
        if is_valid(email, password):
            session['email'] = email
            flash('login successful')
            return redirect(url_for('index'))
        else:
            error = 'Invalid UserId / Password'
            flash('login failed')
            return render_template('login.html', error=error)
    else:
        flash('login failed')
        return render_template('login.html')

## Index
@app.route("/index", methods = ['POST', 'GET'])
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        loggedIn, userName = getLoginDetails()
        sql = "SELECT avatar_url FROM users WHERE email = ?"
        params = [session['email']]
        avatar_url = query.query(sql, params)

        #get username
        sql = "SELECT name, avatar_url, email FROM users" 
        users = query.query_no(sql)

        return render_template("index.html",userName = userName,avatar_url=avatar_url[0][0],users = users)

## Chatroom
@app.route("/chatroom", methods = ['POST', 'GET'])
def chatroom():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        loggedIn, userName = getLoginDetails()

        sql = "SELECT messages.message, messages.created_at, users.name, users.avatar_url, messages.user_id \
                FROM chat.messages,chat.users where messages.user_id = users.id"
        message = query.query_no(sql)

        if message is None:
            message = list()

        sql = "SELECT name, avatar_url FROM users"
        users = query.query_no(sql)

        sql = "SELECT avatar_url FROM users WHERE email = ?"
        params = [session['email']]

        avatar_url = query.query(sql, params)

        return render_template("chatroom.html",userName = userName, message = message, users = users, avatar_url = avatar_url)

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

    join_room(room_name)
    emit('status', {'server_to_client': user_name + ' enter the room'}, room=room_name)

## receive chat messages
@socketio.on('text', namespace='/chatroom')
def text(information):
    text = information.get('text')

    # get username
    user_name = session.get('user') 
    
    # Get user ID
    sql = "SELECT id FROM users WHERE email = ?"
    params = [session['email']]
    user_id = query.query(sql, params)

    # Insert chat information into database, update database
    sql = 'INSERT INTO chatroom.messages (content,user_id) VALUES (?, ?)'
    params = [text, user_id]
    msg = query.update(sql, params)

    create_time = datetime.datetime.now()
    create_time = datetime.datetime.strftime(create_time, '%Y-%m-%d %H:%M:%S')
    
    # Get user avatar
    sql = "SELECT avatar_url FROM users WHERE email = ?"
    params = [session['email']]
    avatar_url = query.query(sql, params)  
    
    # Return the chat information to the front end
    emit('message', {
        'user_name': user_name,
        'text': text,
        'create_time': create_time,
        'avatar_url':avatar_url,
    })

# Connect Home
@socketio.on('Iconnect', namespace='/index')
def Iconnect():
    print('connection succeeded')

# The path to receive the replaced avatar
@socketio.on('avatar_url' ,namespace='/index')
def avatar_url(information):
    email = session['email']
    avatar_url = information.get('avatar_url')
    sql = "UPDATE users SET avatar_url = ? WHERE email = ? "
    params = [avatar_url,email]
    msg = query.update(sql, params)
    print(msg)

if __name__ == '__main__':
    socketio.run(app)