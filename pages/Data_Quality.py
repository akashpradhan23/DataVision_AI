from utils.quality import (
    get_dataset_summary,
    get_missing_values,
    calculate_quality_score
)
import streamlit as st
from utils.quality import get_dataset_summary, get_missing_values

st.set_page_config(
    page_title="Data Quality",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Quality Report")

# Check whether a dataset has been uploaded
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠ Please upload a dataset first.")
    st.stop()

# Get dataset from Session State
df = st.session_state.df

# Get summary
summary = get_dataset_summary(df)
score = calculate_quality_score(df)

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Rows", summary["rows"])
col2.metric("Columns", summary["columns"])
col3.metric("Missing Values", summary["missing_values"])

col4, col5 = st.columns(2)

col4.metric("Duplicate Rows", summary["duplicate_rows"])
col5.metric("Memory Usage (MB)", summary["memory_usage"])

st.divider()
st.subheader("Missing Values by Column")
missing_df = get_missing_values(df)
st.dataframe(missing_df, use_container_width=True)

st.divider()

st.subheader("📈 Data Quality Score")

st.metric("Quality Score", f"{score}/100")

st.progress(score / 100)

if score >= 90:
    st.success("🟢 Excellent Dataset")

elif score >= 70:
    st.warning("🟡 Good Dataset, but needs some cleaning.")

else:
    st.error("🔴 Poor Dataset. Cleaning is recommended before analysis.")