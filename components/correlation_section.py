import streamlit as st
from utils.insights import generate_correlation_insights


def display_correlations(df):
    """
    Display strong correlation insights.
    """

    st.subheader("🔥 Correlation Insights")

    correlations = generate_correlation_insights(df)

    if len(correlations) == 0:
        st.info("No strong correlations found.")

    else:
        for item in correlations:

            with st.container(border=True):

                st.markdown(
                    f"### {item['column1']} ↔ {item['column2']}"
                )

                st.metric(
                    "Correlation",
                    item["correlation"]
                )

                st.success(item["relation"])
                st.info(item["explanation"])