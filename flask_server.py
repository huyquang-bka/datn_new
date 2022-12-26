import time
import cv2
from flask import Flask, Response, render_template, request, redirect, url_for
from threading import Thread
from queue import Queue
import pandas as pd
import numpy as np


app = Flask(__name__, template_folder="resources/templates")

capture_queue = Queue()
stop_thread = False

@app.route('/')
def index():
    return "Hello World"


def gen(capture_queue: Queue):
    t1 = Thread(target=capture, args=(capture_queue, ), daemon=True)
    t1.start()
    while True:
        if capture_queue.empty():
            time.sleep(0.001)
            continue
        image = capture_queue.get()
        image = cv2.resize(image, (640, 480))
        image = cv2.putText(image, str(time.time()), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.5)


@app.route('/video')
def video():
    return Response(gen(capture_queue), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stop')
def video_stop():
    global stop_thread
    stop_thread = True
    return "Stop video"


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
            

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6299)