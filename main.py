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
w, h = 640, 480

def on_btn_start():
    with col1.container():
        st.markdown(
            f"""<img src="{START_CAMERA_URL}" width="{w}" height="{h}" alt="Camera Live">""", unsafe_allow_html=True)
    with col2.container():
        st.markdown(
        f"""<iframe src="{CHART_URL}" width="{w}" height="{h}" allowfullscreen></iframe>""", unsafe_allow_html=True)


def on_btn_stop():
    with col1.container():
        requests.get(STOP_URL)
        image = cv2.imread("stop.png")
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.markdown("Camera stopped")
        col1.image(rgb, width=640)
        
col1, col2 = st.columns([1, 1])
# fps_col, count_col = st.columns([1, 1])
btn_start = col1.button("Start", on_click=on_btn_start, key="btn_start")
btn_stop = col2.button("Stop", key="btn_stop", on_click=on_btn_stop)