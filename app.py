import streamlit as st
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)
hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
st.markdown(hide_footer_style, unsafe_allow_html=True)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
hide_streamlit_style = """
<style>
.css-1y0tads {padding-top: 0rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.header("CRUD Portal ")
#st.set_page_config(page_title="home")

if st.button('View Pages'):
    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
    # Force an app rerun after switching the sidebar state.
    st.experimental_rerun()
st.write("Welcome to the CRUD Portal for the Neuron Ex Chatbot. This Portal offers to do all the document operations in the pinecone database at a single location.")


