import time
from google import genai
import streamlit as st


client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def generate_response(prompt):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(5 * (2 ** attempt))
            else:
                raise


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

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(5 * (2 ** attempt))
            else:
                raise


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

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )
            return response.text

        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(5 * (2 ** attempt))
            else:
                raise