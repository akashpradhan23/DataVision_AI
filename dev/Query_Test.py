import streamlit as st

from ai.query_parser import parse_query

st.title("🧪 Query Parser Test")

question = st.text_input("Enter Question")

columns = [
    "Order_ID",
    "Customer_Age",
    "Region",
    "City",
    "Quantity",
    "Rating",
    "Total_Amount"
]

if st.button("Parse"):

    result = parse_query(
        question,
        columns
    )

    st.json(result)