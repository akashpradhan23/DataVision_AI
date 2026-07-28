import streamlit as st
from utils.visualization import get_dashboard_metrics


def display_kpis(df):
    """
    Display dashboard KPI cards.
    """

    metrics = get_dashboard_metrics(df)

    st.subheader("📌 Dashboard KPIs")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric("Rows", metrics["rows"])

    with kpi2:
        st.metric("Numeric Columns", metrics["numeric_columns"])

    with kpi3:
        st.metric("Average", metrics["average"])

    with kpi4:
        st.metric("Maximum", metrics["maximum"])