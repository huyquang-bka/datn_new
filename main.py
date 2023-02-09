from datetime import datetime
import streamlit as st
import cv2
import pandas as pd
import numpy as np
from main_app.util.tools import *
import requests
from resources.config import *
import sqlite3

conn = sqlite3.connect("traffic.db", check_same_thread=False)
# setup streamlit
st.set_page_config(layout="wide", page_title="Traffic App",
                   page_icon=":car:", initial_sidebar_state="expanded")


# create columns video and chart
w, h = 480, 270

def on_btn_start():
    col1, col2 = st.columns(2)
    col1.write(
        f"""<img src="{START_CAMERA_URL}" object-fit="contain" width="{w}" height="{h}" class="center">""", unsafe_allow_html=True)
    # with col2.container():
    col2.markdown(
        f"""<iframe src="{CHART_URL}" object-fit="contain" width="{480}" height="{360}" allowfullscreen></iframe>""", unsafe_allow_html=True)


def on_btn_stop():
    requests.get(STOP_URL)
    st.write(
        "<h1 style='text-align: center; color: Red;'>Camera stopped</h1>", unsafe_allow_html=True)


options = st.sidebar.selectbox("Select option", ["Dashboard", "Statistic"])
if options == "Dashboard":
    st.markdown("<h1 style='text-align: center; color: white;'>## Dash Board</h1>",
                unsafe_allow_html=True)
    # col1, _, col2 = st.columns([2, 1, 1])
    # fps_col, count_col = st.columns([1, 1])
    btn_start = st.button("Start", key="btn_start")
    btn_stop = st.button("Stop", key="btn_stop")
    if btn_start:
        on_btn_start()
    if btn_stop:
        on_btn_stop()

if options == "Statistic":
    radio_options = st.sidebar.radio(
        "Select option", ["By Day", "By Time", "By Most Traffic Jam"])
    if radio_options == "By Day":
        st.markdown(
            "<h1 style='text-align: center; color: white;'>## Statistic By Day</h1>", unsafe_allow_html=True)
        date = st.date_input(
            "", value=datetime.now().date())
        btn_submit = st.button("Submit")
        if btn_submit:
            col1, col2 = st.columns([3, 1])
            df = pd.read_sql_query(
                con=conn, sql=f"SELECT * FROM traffic WHERE date = '{date}'")
            if len(df) > 0:
                car = df["car"].sum()
                motorbike = df["motorbike"].sum()
                df_bar = pd.DataFrame({"car": [car], "motorbike": [motorbike]})
                col1.bar_chart(df_bar, height=300)
                col2.table(pd.DataFrame(
                    {"car": [car], "motorbike": [motorbike]}))
            else:
                col1.markdown(
                    "<h1 style='text-align: center; color: white;'>## No data</h1>", unsafe_allow_html=True)
    elif radio_options == "By Time":
        st.markdown(
            "<h1 style='text-align: center; color: white;'>## Statistic By Time</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1.container():
            start_date = st.date_input(
                "Start date", value=datetime.now().date())
            start_time = st.time_input(
                "Start time", value=datetime.strptime("00:00", "%H:%M").time())
        with col2.container():
            end_date = st.date_input(
                "End date", value=datetime.now().date())
            end_time = st.time_input("End time", value=datetime.now().time())
        btn_submit = st.button("Submit")
        if btn_submit:
            for date in pd.date_range(start_date, end_date):
                date = date.strftime("%Y-%m-%d")
                with st.container():
                    st.markdown(
                        "<h1 style='text-align: left; color: Green;'>{}</h1>".format(date), unsafe_allow_html=True)
                    col1, col2 = st.columns([3, 1])
                    df = pd.read_sql_query(
                        con=conn, sql=f"SELECT * FROM traffic WHERE date = '{date}'")
                    if len(df) > 0:
                        new_df = df[(df["time"] >= start_time.strftime("%H:%M:%S")) & (
                            df["time"] <= end_time.strftime("%H:%M:%S"))]
                        car = sum(new_df["car"])
                        motorbike = sum(new_df["motorbike"])
                        df_bar = pd.DataFrame(
                            {"car": [car], "motorbike": [motorbike]})
                        col1.bar_chart(df_bar, height=300)
                        col2.table(pd.DataFrame(
                            {"car": [car], "motorbike": [motorbike]}))
                    else:
                        col1.markdown(
                            "<h1 style='text-align: center; color: white;'>## No data</h1>", unsafe_allow_html=True)

    elif radio_options == "By Most Traffic Jam":
        date_input = st.date_input("Select date", value=datetime.now().date())
        range_time = st.number_input(
            "Select range time", min_value=1, max_value=24, value=1)
        btn_submit = st.button("Submit")
        if btn_submit:
            df = pd.read_sql_query(
                con=conn, sql=f"SELECT * FROM traffic WHERE date = '{date_input}'")
            max_car = 0
            max_motorbike = 0
            max_df_car = pd.DataFrame()
            max_df_motorbike = pd.DataFrame()
            label_max_car = ""
            label_max_motorbike = ""
            for i in range(0, 24):
                if i + range_time > 23:
                    break
                start_time = datetime.strptime(
                    str(i), "%H").strftime("%H:%M:%S")
                end_time = datetime.strptime(
                    str(i + range_time), "%H").strftime("%H:%M:%S")
                if end_time > "23:59:59":
                    break
                df_temp = df[(df["time"] >= start_time) & (
                    df["time"] <= end_time)]
                if len(df_temp) > 0:
                    sum_car = sum(df_temp["car"])
                    if sum_car > max_car:
                        max_car = sum_car
                        max_df_car = df_temp
                        label_max_car = start_time + " - " + end_time
                    sum_motorbike = sum(df_temp["motorbike"])
                    if sum_motorbike > max_motorbike:
                        max_motorbike = sum_motorbike
                        max_df_motorbike = df_temp
                        label_max_motorbike = start_time + " - " + end_time
            if len(max_df_car) > 0:
                with st.container():
                    st.markdown(
                        f"<h1 style='text-align: center; color: green;'>{label_max_car}</h1>", unsafe_allow_html=True)
                    col1, col2 = st.columns([2, 1])
                    # col1.title(label_max_car)
                    car = sum(max_df_car["car"])
                    motorbike = sum(max_df_car["motorbike"])
                    col1.bar_chart(pd.DataFrame(
                        {"car": [car], "motorbike": [motorbike]}))
                    # col2.title(label_max_car)
                    col2.table(pd.DataFrame(
                        {"car": [car], "motorbike": [motorbike]}))
            if len(max_df_motorbike) > 0:
                with st.container():
                    st.markdown(
                        f"<h1 style='text-align: center; color: green;'>{label_max_motorbike}</h1>", unsafe_allow_html=True)
                    col1, col2 = st.columns([2, 1])
                    car = sum(max_df_motorbike["car"])
                    motorbike = sum(max_df_motorbike["motorbike"])
                    col1.bar_chart(pd.DataFrame(
                        {"car": [car], "motorbike": [motorbike]}))
                    col2.table(pd.DataFrame(
                        {"car": [car], "motorbike": [motorbike]}))
