import streamlit as st
import cv2
import pandas as pd
import numpy as np
from main_app.util.tools import *
import requests 
from resources.config import *


#setup streamlit
st.set_page_config(layout="wide", page_title="Traffic App", page_icon=":car:", initial_sidebar_state="collapsed")

#sidebar
file_uploader = st.sidebar.file_uploader("Choose video", type=["mp4", "avi", "mov", "mkv"], key="file_uploader", accept_multiple_files=False)
if file_uploader is not None:
    st.sidebar.write("File uploaded")
    with open("resources/Video/video.mp4", "wb") as f:
        f.write(file_uploader.getbuffer())
    st.sidebar.write("File saved")
    st.title("Dashboard Monitor")
    
    #create columns video and chart
    col1, col2 = st.columns([2, 1])
    with col1.container():
        st.markdown(f"""<img src="{VIDEO_URL}" alt="My image">""", unsafe_allow_html=True)
    with col2.container():
        st.markdown(f"""<iframe src="{CHART_URL}" width="640" height="360" frameborder="0" allowfullscreen></iframe>""", unsafe_allow_html=True)

    #create columns fps and count
    fps_col, count_col = st.columns([1, 1])
    fps_col.markdown("""<h1 style="text-align: center; color: red;">FPS: 0</h1>""", unsafe_allow_html=True)
    count_col.markdown("""<h1 style="text-align: center; color: green;">Count: 0</h1>""", unsafe_allow_html=True)
    with fps_col.container():
        



