import streamlit as st

from ai.gemini import analyze_dataset, explain_analysis
from ai.question_router import get_question_type
from ai.query_parser import parse_query

from utils.dataset_summary import generate_dataset_summary
from utils.analytics_engine import run_analysis
from utils.chart_generator import create_chart
from utils.chart_exporter import save_chart

st.set_page_config(page_title="AI Chat", page_icon="💬")

st.title("💬 AI Chat with Your Dataset")
st.write("Ask questions about your uploaded dataset.")

# --------------------------------------------------
# Check Dataset
# --------------------------------------------------
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state.df

rows = df.shape[0]
columns = df.shape[1]

dataset_info = generate_dataset_summary(df)

# --------------------------------------------------
# Dataset Information
# --------------------------------------------------
st.success("✅ Dataset Loaded Successfully!")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", rows)

with col2:
    st.metric("Columns", columns)

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# --------------------------------------------------
# User Question
# --------------------------------------------------
user_question = st.text_input(
    "Ask a question about your dataset:",
    placeholder="Example: Which city generated the highest revenue?"
)

# --------------------------------------------------
# Ask AI
# --------------------------------------------------
if st.button("🚀 Ask AI"):

    if not user_question.strip():
        st.warning("Please enter a question.")
        st.stop()

    question_type = get_question_type(user_question)

    st.info(f"Detected Question Type: **{question_type}**")

    # ==========================================================
    # GENERAL QUESTIONS
    # ==========================================================
    if question_type == "general":

        with st.spinner("🤖 Gemini is analysing..."):

            response = analyze_dataset(
                user_question,
                dataset_info
            )

        st.subheader("🤖 AI Response")
        st.markdown(response)

    # ==========================================================
    # ANALYTICS QUESTIONS
    # ==========================================================
    else:

        with st.spinner("📊 Analysing your data..."):

            parsed = parse_query(
                user_question,
                df.columns.tolist()
            )

            st.subheader("🔍 Parsed Query")
            st.json(parsed)

            analysis = run_analysis(
                df=df,
                analysis_type=parsed.get("analysis_type", ""),
                operation=parsed.get("operation", ""),
                value_column=parsed.get("value_column", ""),
                group_by=parsed.get("group_by", ""),
                ranking=parsed.get("ranking", "")
            )

        # --------------------------------------------------
        # Error Handling
        # --------------------------------------------------
        if "error" in analysis:

            st.error(analysis["error"])

        else:

            st.subheader("📈 Analysis Result")

            # ==========================================
            # SIMPLE ANALYSIS
            # ==========================================
            if analysis["analysis_type"] == "simple":

                st.metric(
                    label=analysis["column"],
                    value=analysis["result"]
                )

            # ==========================================
            # GROUPBY ANALYSIS
            # ==========================================
            elif analysis["analysis_type"] == "groupby":

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        label=f"Top {analysis['group_by']}",
                        value=analysis["best_group"]
                    )

                with col2:
                    st.metric(
                        label=analysis["operation"].title(),
                        value=analysis["best_value"]
                    )

                st.subheader("📋 Result Table")
                st.dataframe(
                    analysis["table"].reset_index(),
                    use_container_width=True
                )

                # ---------------------------------------
                # Automatic Chart
                # ---------------------------------------
                fig = create_chart(analysis)

                if fig:

                    st.subheader("📊 Visualization")

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    # ---------------------------------------
                    # Save Chart for AI Report
                    # ---------------------------------------
                    try:
                        chart_path = save_chart(
                            fig,
                            "analysis_chart.png"
                        )

                        # Store chart path for report page
                        st.session_state["report_chart"] = chart_path

                        st.success("✅ Chart saved for AI Report.")

                    except Exception as e:
                        st.warning(f"Unable to save chart: {e}")

            # --------------------------------------------------
            # Gemini Explanation
            # --------------------------------------------------
            with st.spinner("🤖 Generating AI explanation..."):

                explanation = explain_analysis(
                    user_question,
                    analysis
                )

            st.subheader("💡 AI Explanation")
            st.markdown(explanation)