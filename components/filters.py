import streamlit as st
from utils.visualization import get_categorical_columns


def sidebar_filters(df):
    """
    Display sidebar filters and return the filtered dataframe.
    """

    st.sidebar.header("🔍 Filters")

    categorical_columns = get_categorical_columns(df)

    if len(categorical_columns) > 0:

        selected_filter = st.sidebar.selectbox(
            "Filter Column",
            ["None"] + categorical_columns
        )

        if selected_filter != "None":

            filter_values = sorted(df[selected_filter].dropna().unique())

            selected_value = st.sidebar.selectbox(
                "Select Value",
                filter_values
            )

            df = df[df[selected_filter] == selected_value]

    return df