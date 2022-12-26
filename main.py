import streamlit as st

st.markdown(f"""
    <iframe src="http://localhost:6299/realtime-chart"
            style="border:none;width:500px;height:300px;">
    </iframe>)
    """,
    unsafe_allow_html=True)
