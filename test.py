from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from threading import Lock

app = Flask(__name__, template_folder="resources/templates")
socketio = SocketIO(app, cors_allowed_origins="*")

thread = None
thread_lock = Lock()

def get_new_text():
    # Replace this with a function to retrieve the new text
    return {"fps": datetime.now().strftime("%H:%M:%S"), "count": datetime.now().strftime("%y%m%d %H:%M:%S")}

def background_thread():
    print("Generating random sensor values")
    while True:
        text = get_new_text()
        socketio.emit('dict_update', text, broadcast=True)
        socketio.sleep(1)

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    
@app.route('/text')
def index():
    return render_template("text.html")


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=6299)