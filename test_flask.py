import random
import plotly.express as px
from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__, template_folder="resources/templates")

@app.route('/data')
def data():
    # Generate some random data for the four categories
    data = {
        "car": random.randint(0, 100),
        "truck": random.randint(0, 100),
        "bus": random.randint(0, 100),
        "motorbike": random.randint(0, 100),
    }
    return jsonify(data)

@app.route("/chart")
def realtime_chart():
    return render_template("chart.html")


if __name__ == "__main__":
    app.run(debug=False, port=6299, host="0.0.0.0")