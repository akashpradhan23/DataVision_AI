from google import genai
import streamlit as st

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# ======================================================
# General Chat
# ======================================================

def generate_response(prompt):

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text


# ======================================================
# Dataset Q&A
# ======================================================

def analyze_dataset(question, dataset_info):

    prompt = f"""
You are an expert Data Analyst.

Dataset Summary:

{dataset_info}

Answer the user's question using only the information available in the dataset summary.

If the answer cannot be determined from the dataset summary, clearly say so.

User Question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text


# ======================================================
# Explain Analysis Result
# ======================================================

def explain_analysis(question, analysis_result):

    prompt = f"""
You are an expert Data Analyst.

A user asked:

"{question}"

The analytics engine produced the following result:

{analysis_result}

Explain the result in simple, professional language.

Rules:

- Keep the answer concise.
- Do not mention Python or code.
- If the result contains an error, explain the error politely.
- If the result is a grouped analysis, mention the top group and its value.
- Use bullet points only if they improve readability.
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text