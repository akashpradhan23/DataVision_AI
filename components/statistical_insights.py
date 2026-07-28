import streamlit as st
from utils.insights import generate_basic_insights


def display_statistical_insights(df):
    """
    Display statistical insights for all numeric columns.
    """

    st.subheader("📈 Statistical Insights")

    insights = generate_basic_insights(df)

    for insight in insights:

        with st.expander(f"📊 {insight['column']}"):

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Mean", insight["mean"])
                st.metric("Median", insight["median"])
                st.metric("Standard Deviation", insight["std"])

            with col2:
                st.metric("Minimum", insight["minimum"])
                st.metric("Maximum", insight["maximum"])