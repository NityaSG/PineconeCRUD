import streamlit as st
from pinecone import Pinecone
from datetime import datetime
from openai import OpenAI

# Initialize session state for sidebar if not already done
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

# Configure Streamlit page settings
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)

# CSS to hide Streamlit's footer
hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    </style>
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)

# UI for user to enter their OpenAI API key
openai_api_key = st.text_input("Enter your OpenAI API key", type="password")

# UI for user to enter their Pinecone API key
pinecone_api_key = st.text_input("Enter your Pinecone API key", type="password")

if openai_api_key and pinecone_api_key:
    # Initialize the OpenAI client with the user-provided API key
    client = OpenAI(api_key=openai_api_key)
    
    # Initialize the Pinecone client with the user-provided API key
    pc = Pinecone(api_key=pinecone_api_key)

    # Select the Pinecone index
    index = pc.Index("faq2")

    # Function to generate a unique ID based on the current datetime
    def generate_unique_id():
        now = datetime.now()
        unique_id = now.strftime("%Y%m%d%H%M%S")
        return unique_id

    # Function to get an embedding for a given text
    def get_embedding(text):
        response = client.embeddings.create(
            input=text,
            dimensions=3072,
            model="text-embedding-3-large"
        )
        return response.data[0].embedding

    # Streamlit UI for entering paragraph
    st.header("FAQ Documents")
    raw_text = st.text_input("Enter your paragraph here")

    if st.button("Submit"):
        # Generate an embedding for the entered text
        embedding = get_embedding(raw_text)
        
        # Generate a unique ID for this entry
        id = generate_unique_id()
        
        # Update the Pinecone index with the new embedding and metadata
        # Ensure values are in the correct format (list of embeddings for a single entry)
        index.upsert(vectors=[{"id":id,"values": embedding,"metadata":{"text": raw_text[:100]}}])
        
        st.success("Uploaded Successfully")
