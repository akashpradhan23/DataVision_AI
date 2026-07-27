import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="InsightForge AI",
    page_icon="🔍",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("🔍 InsightForge AI")
st.subheader("Intelligent Data Investigation Platform")

st.divider()

# -----------------------------
# Introduction
# -----------------------------
st.markdown("""
Welcome to **InsightForge AI**.

This platform will help you:

- 📂 Upload CSV and Excel datasets
- 🧹 Clean data automatically
- 📊 Generate interactive visualizations
- 🤖 Train Machine Learning models
- 🧠 Generate AI-powered insights
- 📄 Export professional reports
""")

st.divider()

# -----------------------------
# About
# -----------------------------
st.success("🚀 Your journey to becoming a Data Scientist starts here!")

st.info("⬅️ In the next phase, we'll add a Dataset Upload page.")