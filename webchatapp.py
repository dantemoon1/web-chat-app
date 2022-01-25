from crypt import methods
from gc import callbacks
import sqlite3
import pandas as pd
from flask import Flask, render_template, request #flask imports
from flask_bootstrap import Bootstrap #bootstrap import
import requests, json #currently unused
from flask_socketio import SocketIO, send, emit #used to connect users for chat

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
    if request.form['username'] =='admin': #admin dashboard to see all users and chats
        c.execute('''SELECT * from users''')
        data = c.fetchall()
        return render_template('admin.html', db = data)
    else:
        c.execute('''SELECT username FROM users WHERE username = ?''',(request.form['username'],)) #check if user already exists
        data = c.fetchall() 
        if len(data) == 0: #if user doesnt exist in the db, insert them into db
            c.execute('''INSERT INTO users (username)
                VALUES
                ('{username}')
                '''.format(username=request.form['username']))
            conn.commit() #save changes
    return render_template('chat.html', uname = request.form['username']) #if not admin, load chat.html and pass the username

@SocketIO.on('message') #handles the actual messaging 
def handle_message(data):
    print('received message: '+data)
    send(data,broadcast=True)

if __name__ == '__main__':
    app.debug= True
    socketio.run(app)
    #app.run(host='0.0.0.0',port=5000)