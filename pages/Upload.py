import streamlit as st
import pandas as pd
from utils.loader import load_dataset

if "df" not in st.session_state:
    st.session_state.df = None

st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    st.session_state.df = load_dataset(uploaded_file)

    df = st.session_state.df

    st.success("Dataset uploaded successfully!")

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.subheader("Dataset Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.subheader("Column Names")

    st.write(list(df.columns))

st.divider()

if st.session_state.df is not None:
    st.success("Dataset is stored in Session State ✅")