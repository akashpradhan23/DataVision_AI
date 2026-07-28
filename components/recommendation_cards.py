import streamlit as st
from utils.recommendation import recommend_visualizations


def display_recommendations(df):
    """
    Display smart chart recommendations.
    """

    st.subheader("🤖 Smart Chart Recommendations")

    recommendations = recommend_visualizations(df)

    cols = st.columns(2)

    for index, recommendation in enumerate(recommendations):

        with cols[index % 2]:
            with st.container(border=True):

                st.markdown(f"### {recommendation['chart']}")
                st.caption(recommendation["reason"])