from crypt import methods
from gc import callbacks
import sqlite3
from flask import Flask, render_template, request #flask imports
from flask_bootstrap import Bootstrap #bootstrap import
from flask_socketio import SocketIO, send, emit #used to connect users for chat
import json

app = Flask(__name__)
import os
SECRET_KEY = os.urandom(32) #generate a random key
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
SocketIO = SocketIO(app)

@app.route('/',methods=['GET','POST']) #the main sign in screen
def hello():
    return render_template('home.html')

@app.route('/chat',methods=['GET','POST']) #the chat screen
def chat():
    conn = sqlite3.connect('user_db') #connect to the user database
    c = conn.cursor()
    c.execute('''SELECT * from messages''')
    messageData = c.fetchall()
    messageList = []
    for i in range(len(messageData)):
        messageList.append(messageData[i][0])
    if request.form['username'] =='admin': #admin dashboard to see all users and chats
        c.execute('''SELECT * from users''')
        data = c.fetchall()
        return render_template('admin.html', db = data, messageData = messageList) #pass the database of users
    else:
        c.execute('''SELECT username FROM users WHERE username = ?''',(request.form['username'],)) #check if user already exists
        data = c.fetchall() 
        if len(data) == 0: #if user doesnt exist in the db, insert them into db
            c.execute('''INSERT INTO users (username)
                VALUES
                ('{username}')
                '''.format(username=request.form['username']))
            conn.commit() #save changes
    return render_template('chat.html', uname = request.form['username'], messageData = messageList) #if not admin, load chat.html and pass the username

@SocketIO.on('message') #handles the actual messaging 
def handle_message(data):
    conn = sqlite3.connect('user_db')
    c = conn.cursor()
    c.execute('''INSERT INTO messages (message)
    VALUES
    ('{message}')'''.format(message=data))
    conn.commit()
    print('received message: '+data)
    send(data,broadcast=True)

if __name__ == '__main__':
    app.debug= True
    socketio.run(app)
    #app.run(host='0.0.0.0',port=5000)