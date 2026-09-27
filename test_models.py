import streamlit as st
from google import genai

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

try:
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents="Say Hello"
    )

    st.success(response.text)

except Exception as e:
    st.error(str(e))