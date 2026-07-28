import streamlit as st

from utils.visualization import (
    get_column_summary,
    create_histogram,
    create_box_plot,
    create_scatter_plot,
    create_correlation_heatmap,
    create_bar_chart,
    create_pie_chart,
    get_categorical_columns
)


def display_charts(df):
    """
    Display all visualization charts.
    """

    # Numeric columns (excluding ID columns)
    numeric_columns = [
        col for col in df.select_dtypes(include=["number"]).columns
        if "id" not in col.lower()
    ]

    summary = get_column_summary(df)

    st.subheader("📋 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", summary["rows"])
        st.metric("Numeric Columns", summary["numeric"])

    with col2:
        st.metric("Columns", summary["columns"])
        st.metric("Categorical Columns", summary["categorical"])

    with col3:
        st.metric("Boolean Columns", summary["boolean"])
        st.metric("Date Columns", summary["datetime"])

    # ==============================
    # Histogram & Box Plot
    # ==============================

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):

            st.subheader("📊 Histogram")
            st.caption("Shows how the values of a numeric column are distributed.")

            selected_column = st.selectbox(
                "Select a numeric column",
                numeric_columns,
                key="histogram"
            )

            fig = create_histogram(df, selected_column)

            st.plotly_chart(fig, width="stretch")

    with col2:
        with st.container(border=True):

            st.subheader("📦 Box Plot")
            st.caption("Helps identify outliers and understand the spread of data.")

            box_column = st.selectbox(
                "Select a numeric column",
                numeric_columns,
                key="boxplot"
            )

            box_fig = create_box_plot(df, box_column)

            st.plotly_chart(box_fig, width="stretch")

    # ==============================
    # Scatter Plot
    # ==============================

    st.markdown("---")

    with st.container(border=True):

        st.subheader("📈 Scatter Plot")
        st.caption("Shows the relationship between two numeric variables.")

        col1, col2 = st.columns(2)

        with col1:
            x_column = st.selectbox(
                "Select X-axis",
                numeric_columns,
                key="scatter_x"
            )

        with col2:
            y_column = st.selectbox(
                "Select Y-axis",
                numeric_columns,
                index=1 if len(numeric_columns) > 1 else 0,
                key="scatter_y"
            )

        scatter_fig = create_scatter_plot(df, x_column, y_column)

        st.plotly_chart(scatter_fig, width="stretch")

    # ==============================
    # Correlation Heatmap
    # ==============================

    st.markdown("---")

    with st.container(border=True):

        st.subheader("🔥 Correlation Heatmap")
        st.caption("Shows the correlation between all numeric columns.")

        heatmap_fig = create_correlation_heatmap(df)

        st.plotly_chart(heatmap_fig, width="stretch")

    # ==============================
    # Bar Chart
    # ==============================

    st.markdown("---")

    with st.container(border=True):

        st.subheader("📊 Bar Chart")
        st.caption("Shows the frequency of each category.")

        categorical_columns = get_categorical_columns(df)

        if len(categorical_columns) > 0:

            selected_category = st.selectbox(
                "Select a categorical column",
                categorical_columns,
                key="bar_chart"
            )

            bar_fig = create_bar_chart(df, selected_category)

            st.plotly_chart(bar_fig, width="stretch")

        else:
            st.info("No categorical columns found.")

    # ==============================
    # Pie Chart
    # ==============================

    st.markdown("---")

    with st.container(border=True):

        st.subheader("🥧 Pie Chart")
        st.caption("Shows the percentage distribution of each category.")

        categorical_columns = get_categorical_columns(df)

        if len(categorical_columns) > 0:

            selected_category = st.selectbox(
                "Select a categorical column",
                categorical_columns,
                key="pie_chart"
            )

            pie_fig = create_pie_chart(df, selected_category)

            st.plotly_chart(pie_fig, width="stretch")

        else:
            st.info("No categorical columns found.")