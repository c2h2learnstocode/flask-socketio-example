from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_apscheduler import APScheduler
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

#function executed by scheduled job
def broadcast_time(text):
    #print(text, str(datetime.datetime.now()))
    xxx=str(datetime.datetime.now())
    with app.test_request_context('/'):
        socketio.emit('message', xxx, namespace='/')    

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


@app.route("/")
def index():
    return render_template("index.html")

if (__name__ == "__main__"):
    scheduler = APScheduler()
    scheduler.add_job(func=broadcast_time, args=['job run'], trigger='interval', id='job', seconds=5)
    scheduler.start()
    app.run(port = 5000)


