import streamlit as st
from components.filters import sidebar_filters
from components.kpi_cards import display_kpis
from components.statistical_insights import display_statistical_insights
from components.outlier_section import display_outliers
from components.correlation_section import display_correlations
from components.recommendation_cards import display_recommendations
from components.charts import display_charts

st.set_page_config(
    page_title="Visualization Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Visualization Dashboard")

# Check if dataset exists
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠ Please upload a dataset first.")
    st.stop()

df = st.session_state.df

df = sidebar_filters(df)


display_kpis(df)

display_statistical_insights(df)

display_outliers(df)

display_correlations(df)

display_recommendations(df)



display_charts(df)