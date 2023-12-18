# streamlit_app.py
import streamlit as st
import json

st.title("Dark Pattern Detection")

# Receive messages from the Chrome extension
dark_patterns_data = st.session_state.get('dark_patterns_data', None)
if dark_patterns_data:
    st.text("Detected Dark Patterns:")
    for d in dark_patterns_data['dark_patterns']:
        st.text(d)
    st.text(f"Number of Detected Dark Patterns: {dark_patterns_data['num_dark_patterns']}")

    st.text("Debugging:")
    st.text(f"Output of presence classifier: {dark_patterns_data['output']}")
else:
    st.text("No dark patterns detected.")
