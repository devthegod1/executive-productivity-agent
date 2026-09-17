import os

# Attempt to read from environment or Streamlit secrets
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    try:
        import streamlit as st
        if "MISTRAL_API_KEY" in st.secrets:
            api_key = st.secrets["MISTRAL_API_KEY"]
    except Exception:
        pass

if not api_key:
    raise ValueError("MISTRAL_API_KEY is not set. Add it to .env or Streamlit Cloud secrets.")