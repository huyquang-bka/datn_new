import streamlit as st
import cv2
import pandas as pd
import numpy as np
from main_app.util.tools import *
import requests
from resources.config import *


# setup streamlit
st.set_page_config(layout="wide", page_title="Traffic App",
                   page_icon=":car:", initial_sidebar_state="collapsed")

# sidebar
st.title("Dashboard Monitor")

# create columns video and chart


def on_btn_start():
    with col1.container():
        st.markdown(
            f"""<img src="{VIDEO_URL}" alt="My image">""", unsafe_allow_html=True)
    with col2.container():
        st.markdown(
            f"""<iframe src="{CHART_URL}" width="640" height="360" frameborder="0" allowfullscreen></iframe>""", unsafe_allow_html=True)

    fps_col.markdown(
        """<h1 style="text-align: center; color: red;">FPS: 0</h1>""", unsafe_allow_html=True)
    count_col.markdown(
        """<h1 style="text-align: center; color: green;">Count: 0</h1>""", unsafe_allow_html=True)


def on_btn_stop():
    with col1.container():
        st.markdown(
            f"""<img src="{open("stop.png", "rb")}" alt="My image">""", unsafe_allow_html=True)


col1, col2 = st.columns([2, 1])
fps_col, count_col = st.columns([1, 1])
btn_start = col1.button("Start", on_click=on_btn_start, key="btn_start")
btn_stop = col1.button("Stop", key="btn_stop", on_click=on_btn_stop)
