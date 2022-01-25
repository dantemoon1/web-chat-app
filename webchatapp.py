from crypt import methods
from gc import callbacks
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
    if request.form['username'] =='admin': #admin dashboard to see all users and chats
        return render_template('admin.html')
    return render_template('chat.html', uname = request.form['username']) #if not admin, load chat.html and pass the username

@SocketIO.on('message') 
def handle_message(data):
    print('received message: '+data)
    send(data,broadcast=True)

if __name__ == '__main__':
    app.debug= True
    socketio.run(app)
    #app.run(host='0.0.0.0',port=5000)