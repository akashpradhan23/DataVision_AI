import streamlit as st

from utils.report_metrics import generate_report_metrics
from utils.dashboard_generator import generate_dashboard
from utils.dataset_summary import generate_dataset_summary
from ai.gemini import generate_response

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataVisoion AI Dashboard")

# ----------------------------------------------------
# Check Dataset
# ----------------------------------------------------
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state.df.copy()

# ----------------------------------------------------
# Sidebar Filters
# ----------------------------------------------------
st.sidebar.header("🔍 Dashboard Filters")

filtered_df = df.copy()

# Region Filter
if "Region" in filtered_df.columns:

    regions = ["All"] + sorted(
        filtered_df["Region"].dropna().unique().tolist()
    )

    selected_region = st.sidebar.selectbox(
        "Select Region",
        regions
    )

    if selected_region != "All":
        filtered_df = filtered_df[
            filtered_df["Region"] == selected_region
        ]

# Product Filter
if "Product" in filtered_df.columns:

    products = ["All"] + sorted(
        filtered_df["Product"].dropna().unique().tolist()
    )

    selected_product = st.sidebar.selectbox(
        "Select Product",
        products
    )

    if selected_product != "All":
        filtered_df = filtered_df[
            filtered_df["Product"] == selected_product
        ]

# ----------------------------------------------------
# Generate Metrics
# ----------------------------------------------------
metrics = generate_report_metrics(filtered_df)

# ----------------------------------------------------
# KPI Dashboard
# ----------------------------------------------------
st.subheader("📈 Dataset Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Rows", metrics["rows"])

with k2:
    st.metric("Columns", metrics["columns"])

with k3:
    st.metric("Missing Values", metrics["missing"])

with k4:
    st.metric("Duplicate Rows", metrics["duplicates"])

# ----------------------------------------------------
# Dataset Structure
# ----------------------------------------------------
st.subheader("📋 Dataset Structure")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Numeric Columns", metrics["numeric"])

with c2:
    st.metric("Categorical Columns", metrics["categorical"])

with c3:
    st.metric("Boolean Columns", metrics["boolean"])

st.divider()

# ----------------------------------------------------
# Dashboard Charts
# ----------------------------------------------------
st.subheader("📊 Business Dashboard")

charts = generate_dashboard(filtered_df)

chart_items = list(charts.items())

for i in range(0, len(chart_items), 2):

    col1, col2 = st.columns(2)

    with col1:
        title, fig = chart_items[i]
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if i + 1 < len(chart_items):

        with col2:
            title, fig = chart_items[i + 1]
            st.plotly_chart(
                fig,
                use_container_width=True
            )

st.divider()

# ----------------------------------------------------
# AI Business Summary
# ----------------------------------------------------
st.subheader("🤖 AI Business Summary")

dataset_summary = generate_dataset_summary(filtered_df)

if st.button(
    "✨ Generate AI Dashboard Summary",
    use_container_width=True
):

    with st.spinner("Generating AI Business Summary..."):

        prompt = f"""
You are a Senior Business Intelligence Analyst.

Below is a dataset summary.

{dataset_summary}

Generate a professional business summary.

Requirements:

• Maximum 8 bullet points.
• Mention important business observations.
• Mention data quality.
• Mention possible improvements.
• Mention trends if available.
• Do not invent facts.
• Keep the language simple and professional.
"""

        summary = generate_response(prompt)

    st.success("✅ AI Summary Generated")

    st.markdown(summary)