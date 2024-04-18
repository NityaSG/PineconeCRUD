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
        "Retirement": "d3dcb4ca-6130-4685-8ecd-a596b2d6b578",
        "Term Insurance": "ef2b66b4-6541-406e-90c3-3461a0175e9e",
        "Health Insurance": "7d079fc8-43da-4645-9610-4646a7e66d2b",
        "Savings Plan": "941be9c1-7d77-4f15-b768-4c59f5b861a4",
        "ULIP Plan": "11ae8662-0cb0-486a-bff7-fb0a1c12d037",
        "Guaranteed Wealth Builder Plans": "46cb7617-a687-403d-8ab4-d2862c9faa5a"
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
