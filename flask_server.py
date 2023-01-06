import time
import cv2
from flask import Flask, Response, jsonify, render_template, request, redirect, url_for
from threading import Thread
from queue import Queue
import pandas as pd
import numpy as np
from main_app.util.detect_yolov5 import Tracking
from main_app.util.tools import count_object, polygon
from datetime import datetime
import sqlite3

app = Flask(__name__, template_folder="resources/templates")
conn = sqlite3.connect("traffic.db", check_same_thread=False)


capture_queue = Queue()
stop_thread = False
count_object_dict = {"car": 0, "motorbike": 0}

tracker = Tracking()
tracker.weights = r"resources/Weight/last_vehicle_23122022.pt"
tracker.imgsz = 640
tracker.device = "cpu"
tracker.conf_thres = 0.1
tracker.classes = [0, 1]
tracker.agnostic_nms = True
tracker.half = False
tracker._load_model()
print("Load model success, names: ", tracker.names)


def capture(capture_queue: Queue):
    global stop_thread, count_object_dict
    path = r"C:\Users\Admin\Downloads\00005.MTS"
    cap = cv2.VideoCapture(path)
    while True:
        ret, image = cap.read()
        if not ret:
            cap = cv2.VideoCapture(path)
            continue
        if capture_queue.empty():
            capture_queue.put(image)
        if stop_thread:
            count_object_dict = {
                "car": 0, "motorbike": 0}
            break
        time.sleep(0.035)


def gen(capture_queue: Queue):
    global stop_thread, count_object_dict
    # stop_thread = True
    # time.sleep(1)
    stop_thread = False
    t1 = Thread(target=capture, args=(capture_queue, ), daemon=True)
    t1.start()
    old_dict = {}
    while True:
        # reset count when time between 00:00:00 and 00:00:10
        now = datetime.now()
        if now.hour == 0 and now.minute == 0 and now.second < 10:
            count_object_dict = {"car": 0, "motorbike": 0}
        if capture_queue.empty():
            time.sleep(0.001)
            continue
        image = capture_queue.get()
        id_dict = tracker.track(image)
        count_dict = count_object(old_dict, id_dict, polygon)
        for key, value in count_dict.items():
            count_object_dict[key] += value
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H:%M:%S")
        df = pd.DataFrame({"date": [date_str], "time": [time_str], "car": [
                          count_dict["car"]], "motorbike": [count_dict["motorbike"]]})
        df.to_sql("traffic", conn, if_exists="append", index=False)
        old_dict = id_dict.copy()
        cv2.polylines(image, [polygon], True, (0, 255, 0), 2)
        for key, value in id_dict.items():
            x1, y1, x2, y2 = value[:4]
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


################################################################################################

@app.route('/')
def index():
    return "Hello World"


@app.route('/data')
def data():
    global count_object_dict
    return jsonify(count_object_dict)


@app.route('/start')
def video():
    return Response(gen(capture_queue), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stop')
def video_stop():
    global stop_thread, count_object_dict
    stop_thread = True
    count_object_dict = {"car": 0, "motorbike": 0}
    return "Stop video"


@app.route('/chart')
def chart():
    return render_template('chart.html')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6299)
