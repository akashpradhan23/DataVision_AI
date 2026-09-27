import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

print("Available Models:\n")

for model in genai.list_models():
    print(f"Name: {model.name}")
    print(f"Supported Methods: {model.supported_generation_methods}")
    print("-" * 50)