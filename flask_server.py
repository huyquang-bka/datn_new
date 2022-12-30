import random
import time
import cv2
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from threading import Thread
from queue import Queue
from datetime import datetime

app = Flask(__name__, template_folder="resources/templates")

socketio = SocketIO(app, cors_allowed_origins="*")

capture_queue = Queue()
stop_thread = False
count = 0
fps = 0
car = 0
bus = 0
truck = 0
motorbike = 0


@app.route('/')
def index():
    return "Hello World"


def gen(capture_queue: Queue):
    global stop_thread, count, fps, car, bus, truck, motorbike
    stop_thread = False
    t1 = Thread(target=capture, args=(capture_queue, ), daemon=True)
    t1.start()
    while True:
        if capture_queue.empty():
            time.sleep(0.001)
            continue
        image = capture_queue.get()
        image = cv2.resize(image, (640, 480))
        image = cv2.putText(image, str(time.time()), (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        motorbike += 4
        car += 3
        truck += 2
        bus += 1
        count = motorbike + car + truck + bus
        fps = datetime.now().strftime("%H:%M:%S")
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.2)


@app.route('/data')
def data():
    # global count, fps, car, bus, truck, motorbike
    new_dict = {"car": random.randint(0, 10), "bus": random.randint(0, 10), "truck": random.randint(0, 10), "motorbike": random.randint(0, 10)}
    return jsonify(new_dict)

@app.route('/realtime-chart')
def realtime_chart():
    return render_template("rt_chart_2.html")

@ app.route('/start')
def video():
    return Response(gen(capture_queue), mimetype='multipart/x-mixed-replace; boundary=frame')


@ app.route('/stop')
def video_stop():
    global stop_thread
    stop_thread = True
    return "Stop video"


@ app.route('/get_count')
def get_count():
    return str(count)


@ app.route('/get_fps')
def get_fps():
    return str(fps)


def capture(capture_queue: Queue):
    global stop_thread
    cap = cv2.VideoCapture(0)
    while True:
        ret, image = cap.read()
        if not ret:
            break
        if capture_queue.empty():
            capture_queue.put(image)
        if stop_thread:
            break
        time.sleep(0.03)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6299)
