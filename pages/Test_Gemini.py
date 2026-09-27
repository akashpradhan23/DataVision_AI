import streamlit as st
from google import genai

st.title("Gemini Test")

try:
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Say hello in one sentence."
    )

    st.success("Gemini is working!")
    st.write(response.text)

except Exception as e:
    st.error("Gemini failed")
    st.write(type(e).__name__)
    st.write(str(e))