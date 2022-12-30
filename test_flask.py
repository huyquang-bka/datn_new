import random
import plotly.express as px
from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__, template_folder="resources/templates")

@app.route("/data")
def data():
    # Generate some random data
    data = {"class_1": random.randint(0, 10), "class_2": random.randint(0, 10), "class_3": random.randint(0, 10)}
    return jsonify(data)

@app.route("/realtime-chart")
def realtime_chart():
    return render_template("rt_chart_2.html")


if __name__ == "__main__":
    app.run(debug=True, port=6299, host="0.0.0.0")