import streamlit as st
from ai.gemini import generate_response

st.title("🤖 Gemini AI Test")

prompt = st.text_area("Enter your question:")

if st.button("Ask Gemini"):
    if prompt.strip():
        response = generate_response(prompt)
        st.success(response)
    else:
        st.warning("Please enter a question.")