import streamlit as st

st.set_page_config(
    page_title="CyberRAG",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ CyberRAG")

st.subheader("AI-powered Cybersecurity Knowledge Assistant")

st.write(
    """
    Welcome to CyberRAG!

    This application will allow security analysts to query
    cybersecurity knowledge using natural language.
    """
)

st.success("Frontend is running successfully!")
