import streamlit as st
from pinecone import Pinecone
from openai import OpenAI

# Streamlit UI adjustments
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)
hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    </style>
    """
st.markdown(hide_footer_style, unsafe_allow_html=True)

# Prompt the user to enter their OpenAI and Pinecone API keys
openai_api_key = st.text_input("Enter your OpenAI API key", type="password")
pinecone_api_key = st.text_input("Enter your Pinecone API key", type="password")

# Only proceed if both API keys are provided
if openai_api_key and pinecone_api_key:
    # Initialize the OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Dictionary mapping types to IDs
    id = {
        "Retirement": "fb426e47-6a0e-4474-b041-9cd424f56bec",
        "Term Insurance": "544192f1-d025-49f4-90b1-898b5fd12a74",
        "Health Insurance": "2fbc4a5d-2a72-472e-bdb4-116db1cce371",
        "Savings Plan": "2fbc4a5d-2a72-472e-bdb4-116db1cce371",
        "ULIP Plan": "eba418c1-3a58-4174-a8b4-131bb6525feb",
        "Guaranteed Wealth Builder Plans": "2fd100ff-5328-49c5-a39b-7f4c7c1a898f"
    }

    # Function to get embedding
    def get_embedding(text):
        response = client.embeddings.create(
            input=text,
            dimensions=3072,
            model="text-embedding-3-large"
        )
        return response.data[0].embedding

    # Streamlit UI for main content
    st.header("Layer 1 recommendations")

    # Pinecone client initialization with user-provided API key
    pc = Pinecone(api_key=pinecone_api_key)

    # Select the Pinecone index
    index = pc.Index("rec15")

    # Dropdown menu for insurance types
    insurance_type = st.selectbox("Select Insurance Type", options=list(id.keys()))

    # Text input for user to enter their paragraph
    raw_text = st.text_input("Enter your paragraph here")

    if st.button("Submit"):
        # Get the embedding for the entered text
        embedding = get_embedding(raw_text)
        
        # Retrieve the ID for the selected insurance type from the dictionary
        selected_id = id[insurance_type]
        
        # Update the Pinecone index with the new embedding and metadata
        index.update(id=selected_id, values=[embedding], set_metadata={"type": insurance_type})
        
        st.success("Uploaded Successfully")
