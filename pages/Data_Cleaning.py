import io
import streamlit as st
from utils.cleaning import clean_dataset
from utils.quality import get_dataset_summary

st.set_page_config(
    page_title="Data Cleaning",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Data Cleaning")

# Check if dataset exists
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠ Please upload a dataset first.")
    st.stop()

# Get dataset
df = st.session_state.df

st.subheader("Original Dataset")
st.dataframe(df.head())


before_summary = get_dataset_summary(df)

# Cleaning button
if st.button("🧹 Clean Dataset"):

    cleaned_df, stats = clean_dataset(df)

    st.session_state.cleaned_df = cleaned_df

    after_summary = get_dataset_summary(cleaned_df)

    st.success("✅ Dataset cleaned successfully!")

    st.info(f"""
### 🧹 Cleaning Report

✅ Duplicate rows removed: **{stats['duplicates_removed']}**

✅ Missing values filled: **{stats['missing_values_filled']}**
""")

    st.subheader("Cleaning Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Before Cleaning")
        st.metric("Rows", before_summary["rows"])
        st.metric("Missing Values", before_summary["missing_values"])
        st.metric("Duplicate Rows", before_summary["duplicate_rows"])

    with col2:
        st.markdown("### After Cleaning")
        st.metric("Rows", after_summary["rows"])
        st.metric("Missing Values", after_summary["missing_values"])
        st.metric("Duplicate Rows", after_summary["duplicate_rows"])

    st.subheader("Cleaned Dataset")
    st.dataframe(cleaned_df.head())

    

    st.subheader("Cleaned Dataset")
    st.dataframe(cleaned_df.head())

    csv = cleaned_df.to_csv(index=False)

    st.download_button(
        label="📥 Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )