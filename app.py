import streamlit as st

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="DataVision AI",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("📊 DataVision AI")
st.caption("AI-Powered Data Analytics & Business Intelligence Platform")
st.subheader("Intelligent Data Investigation Platform")

st.divider()

# -----------------------------
# Introduction
# -----------------------------
st.markdown("""
Welcome to **DataVision AI**.

This platform helps you:

- 📂 Upload CSV and Excel datasets
- 🧹 Clean data automatically
- 📊 Generate interactive visualizations
- 🤖 Train Machine Learning models
- 🧠 Generate AI-powered insights
- 💬 Chat with your data using AI
- 📄 Export professional reports
""")

st.divider()

# -----------------------------
# About
# -----------------------------
st.success("🚀 Transform your data into intelligent decisions with AI.")

st.info("⬅️ Select a module from the sidebar to begin your analysis.")