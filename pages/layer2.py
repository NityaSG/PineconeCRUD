import streamlit as st
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)
hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
st.title("Layer 2 recommendation Document")

st.write("Comming soon.... ")