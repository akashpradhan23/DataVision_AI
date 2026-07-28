import streamlit as st

from ai.gemini import analyze_dataset
from ai.prompts import DATASET_ANALYSIS_PROMPT
from utils.dataset_summary import generate_dataset_summary

st.set_page_config(page_title="AI Insights", page_icon="🤖")

st.title("🤖 AI Dataset Insights")
st.write("Generate AI-powered insights for your uploaded dataset.")

# Check if dataset is uploaded
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("Please upload a dataset first.")
    st.stop()

# Get the uploaded DataFrame
df = st.session_state.df

# Generate dataset summary
dataset_info = generate_dataset_summary(df)

# Analyze button
if st.button("🔍 Analyze Dataset"):
    with st.spinner("🤖 Gemini is analyzing your dataset..."):
        result = analyze_dataset(
            DATASET_ANALYSIS_PROMPT,
            dataset_info
        )

    st.markdown(result)