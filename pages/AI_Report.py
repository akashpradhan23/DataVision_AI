import streamlit as st
import os

from ai.gemini import generate_response
from utils.dataset_summary import generate_dataset_summary
from utils.report_metrics import generate_report_metrics
from utils.report_statistics import generate_statistics
from report.pdf_generator import generate_pdf

st.set_page_config(
    page_title="AI Report",
    page_icon="📄"
)

st.title("📄 AI Report Generator")

# ----------------------------------------------------
# Check Dataset
# ----------------------------------------------------
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state.df

# ----------------------------------------------------
# Generate Dataset Information
# ----------------------------------------------------
dataset_summary = generate_dataset_summary(df)
metrics = generate_report_metrics(df)
statistics = generate_statistics(df)

# ----------------------------------------------------
# Dataset Summary
# ----------------------------------------------------
st.subheader("📄 Dataset Summary")
st.write(dataset_summary)

# ----------------------------------------------------
# KPI Dashboard
# ----------------------------------------------------
st.subheader("📊 Dataset KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", metrics["rows"])

with col2:
    st.metric("Columns", metrics["columns"])

with col3:
    st.metric("Missing Values", metrics["missing"])

with col4:
    st.metric("Duplicate Rows", metrics["duplicates"])

# ----------------------------------------------------
# Data Types
# ----------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Numeric Columns", metrics["numeric"])

with col2:
    st.metric("Categorical Columns", metrics["categorical"])

with col3:
    st.metric("Boolean Columns", metrics["boolean"])

# ----------------------------------------------------
# Descriptive Statistics
# ----------------------------------------------------
st.subheader("📈 Descriptive Statistics")

for column, values in statistics.items():

    with st.expander(f"📊 {column}"):

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Mean", values["Mean"])
            st.metric("Minimum", values["Minimum"])
            st.metric("Std Dev", values["Std Dev"])

        with c2:
            st.metric("Median", values["Median"])
            st.metric("Maximum", values["Maximum"])

# ----------------------------------------------------
# Generate AI Report
# ----------------------------------------------------
st.divider()

if st.button("📄 Generate AI Report", use_container_width=True):

    with st.spinner("🤖 Generating Professional AI Report..."):

        prompt = f"""
You are a Senior Business Intelligence Analyst.

Generate a professional business report.

Dataset Summary:

{dataset_summary}

Dataset Metrics:

Rows: {metrics["rows"]}
Columns: {metrics["columns"]}
Missing Values: {metrics["missing"]}
Duplicate Rows: {metrics["duplicates"]}

Write the report using EXACTLY these headings:

Executive Summary

Dataset Overview

Data Quality

Key Findings

Business Insights

Recommendations

Conclusion

Rules:

- Write professionally.
- Keep paragraphs concise.
- Use bullet points wherever appropriate.
- Do NOT invent information.
- Base everything ONLY on the dataset summary and metrics.
"""

        report = generate_response(prompt)

        os.makedirs("reports", exist_ok=True)

        pdf_path = "reports/DataVision_Report.pdf"

        # --------------------------------------------
        # Get saved visualization
        # --------------------------------------------
        chart_path = st.session_state.get(
            "report_chart",
            None
        )

        generate_pdf(
            filename=pdf_path,
            title="DataVision AI Report",
            report=report,
            chart_path=chart_path
        )

    st.success("✅ AI Report Generated Successfully!")

    # ----------------------------------------------------
    # Report Preview
    # ----------------------------------------------------
    st.subheader("📑 Report Preview")
    st.markdown(report)

    # ----------------------------------------------------
    # Statistics Preview
    # ----------------------------------------------------
    st.subheader("📊 Statistics Used")

    st.dataframe(
        df.describe().T,
        use_container_width=True
    )

    # ----------------------------------------------------
    # Chart Preview
    # ----------------------------------------------------
    if chart_path and os.path.exists(chart_path):

        st.subheader("📈 Included Visualization")

        st.image(
            chart_path,
            use_container_width=True
        )

    # ----------------------------------------------------
    # Download PDF
    # ----------------------------------------------------
    with open(pdf_path, "rb") as file:

        st.download_button(
            label="⬇ Download AI Report",
            data=file,
            file_name="DataVision_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )