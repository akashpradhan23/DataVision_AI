import json
from google import genai
import streamlit as st

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


def parse_query(question, columns):

    prompt = f"""
You are an AI Data Analytics Query Parser.

Dataset Columns:

{columns}

Understand the user's question.

Return ONLY valid JSON.

The JSON format MUST be:

{{
    "analysis_type":"",
    "operation":"",
    "value_column":"",
    "group_by":"",
    "ranking":""
}}

Rules:

1. analysis_type can only be:
- simple
- groupby

2. operation can only be:
- mean
- sum
- max
- min
- count

3. value_column MUST exactly match one dataset column.

4. group_by MUST exactly match one dataset column if required, otherwise leave it empty.

5. ranking can only be:
- highest
- lowest

Leave ranking empty if not required.

Examples

Question:
What is the average customer age?

Return

{{
    "analysis_type":"simple",
    "operation":"mean",
    "value_column":"Customer_Age",
    "group_by":"",
    "ranking":""
}}

Question:
What is the maximum rating?

Return

{{
    "analysis_type":"simple",
    "operation":"max",
    "value_column":"Rating",
    "group_by":"",
    "ranking":""
}}

Question:
Which city generated the highest revenue?

Return

{{
    "analysis_type":"groupby",
    "operation":"sum",
    "value_column":"Total_Amount",
    "group_by":"City",
    "ranking":"highest"
}}

Question:
Which region has the lowest sales?

Return

{{
    "analysis_type":"groupby",
    "operation":"sum",
    "value_column":"Total_Amount",
    "group_by":"Region",
    "ranking":"lowest"
}}

Important Rules:

- Return ONLY JSON.
- Do NOT use markdown.
- Do NOT explain anything.
- Do NOT wrap the JSON inside ```json blocks.

User Question:

{question}
"""
    st.error("USING UPDATED QUERY PARSER")
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini accidentally returns it
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        return json.loads(text)

    except Exception:
        return {
            "analysis_type": "",
            "operation": "",
            "value_column": "",
            "group_by": "",
            "ranking": ""
        }