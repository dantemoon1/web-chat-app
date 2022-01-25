from flask import Flask, render_template #flask imports
import requests, json #currently unused
from flask_socketio import SocketIO #used to connect users for chat

app = Flask(__name__)
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
SocketIO = SocketIO(app)

@app.route('/')
def hello():
    return render_template('home.html')

def received(methods = ['GET','POST']):
    print('the message was received sucessfully')

@SocketIO.on('event')
def handle_message(message,methods=['GET','POST']):
    print('received message:' + str(message))
    SocketIO.emit('my message', message, callback=received)

if __name__ == '__main__':
    app.debug= True
    app.run(host='0.0.0.0',port=5000)