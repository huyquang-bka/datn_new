import streamlit as st

#st markdown html file
col1, col2 = st.columns(2)
col1.markdown("""<div id="text"; style="font-size: 20px; font-weight: bold; color: red;">FPS</div>""", unsafe_allow_html=True)
col2.markdown("""<div id="text"; style="font-size: 20px; font-weight: bold; color: yellow;">Count</div>""", unsafe_allow_html=True)

# with col1.container():
#     st.markdown("""<iframe style="color: red; font-weight: bold;" src="http://localhost:6299/text"></iframe>""", unsafe_allow_html=True)
    
with col2.container():
    st.markdown(open("resources/templates/count.html").read(), unsafe_allow_html=True)