import streamlit as st
from utils.insights import detect_outliers


def display_outliers(df):
    """
    Display outlier detection results.
    """

    st.subheader("🚨 Outlier Detection")

    outliers = detect_outliers(df)

    for item in outliers:

        if item["count"] == 0:
            st.success(f"✅ {item['column']}: No outliers detected.")

        else:
            st.warning(
                f"⚠ {item['column']}: {item['count']} outlier(s) detected."
            )

            with st.expander("View Outlier Records"):
                st.dataframe(item["rows"], use_container_width=True)