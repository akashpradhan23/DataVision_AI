import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle

from utils.model_trainer import train_model

st.set_page_config(
    page_title="Predictive Analytics",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Predictive Analytics (AutoML)")

# ---------------------------------------
# Check Dataset
# ---------------------------------------
if "df" not in st.session_state or st.session_state.df is None:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state.df.copy()

st.success(f"Dataset Loaded Successfully ({df.shape[0]} rows × {df.shape[1]} columns)")

# ---------------------------------------
# Target Selection
# ---------------------------------------
st.subheader("🎯 Select Target Column")

target = st.selectbox(
    "Choose the column you want to predict",
    df.columns
)

# ---------------------------------------
# Train Model
# ---------------------------------------
if st.button("🚀 Train Model", use_container_width=True):

    try:
        with st.spinner("Training multiple machine learning models..."):
            results = train_model(df, target)

            st.session_state["results"] = results
    except Exception as e:
        st.error(f"❌ {e}")
        st.stop()
# ---------------------------------------
# Load Training Results
# ---------------------------------------
if "results" not in st.session_state:
    st.stop()

results = st.session_state["results"]

st.success("✅ Training Completed!")

# ---------------------------------------
# Best Model
# ---------------------------------------
st.subheader("🏆 Best Model")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Problem Type",
        results["problem_type"].title()
    )

with col2:
    st.metric(
        "Best Model",
        results["best_model_name"]
    )

st.divider()

# ---------------------------------------
# Model Comparison
# ---------------------------------------
st.subheader("📊 Model Comparison")

comparison = pd.DataFrame(results["evaluation"]).T

st.dataframe(
    comparison,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# Best Model Metrics
# ---------------------------------------
st.subheader("📈 Best Model Performance")

best_metrics = results["evaluation"][results["best_model_name"]]

cols = st.columns(len(best_metrics))

for i, (metric, value) in enumerate(best_metrics.items()):
    with cols[i]:
        st.metric(metric, value)

st.divider()

# Save Model

st.session_state["trained_model"] = results["best_model"]
st.session_state["target_column"] = target
st.session_state["problem_type"] = results["problem_type"]
st.session_state["feature_columns"] = results["feature_columns"]

st.success("✅ Best model is ready for prediction.")

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================
feature_df = results["feature_importance"]

if feature_df is not None:

    st.divider()
    st.subheader("📊 Feature Importance")

    fig = px.bar(
        feature_df.head(15),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 15 Important Features"
    )

    fig.update_layout(
        yaxis=dict(autorange="reversed")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        feature_df,
        use_container_width=True
    )

# ==========================================================
# ACTUAL VS PREDICTED (Regression)
# ==========================================================
if results["problem_type"] == "regression":

    st.divider()
    st.subheader("📈 Actual vs Predicted")

    ap = results["actual_vs_predicted"]

    fig = px.scatter(
        ap,
        x="Actual",
        y="Predicted",
        title="Actual vs Predicted Values"
    )

    fig.add_shape(
        type="line",
        x0=ap["Actual"].min(),
        y0=ap["Actual"].min(),
        x1=ap["Actual"].max(),
        y1=ap["Actual"].max(),
        line=dict(color="red", dash="dash")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# CONFUSION MATRIX (Classification)
# ==========================================================
else:

    st.divider()
    st.subheader("📉 Confusion Matrix")

    cm = results["confusion_matrix"]

    fig = go.Figure(
        data=go.Heatmap(
            z=cm,
            colorscale="Blues",
            text=cm,
            texttemplate="%{text}",
            hoverongaps=False
        )
    )

    fig.update_layout(
        xaxis_title="Predicted",
        yaxis_title="Actual"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# DOWNLOAD MODEL
# ==========================================================
st.divider()

st.subheader("💾 Download Trained Model")

model_bytes = pickle.dumps(results["best_model"])

st.download_button(
    label="⬇ Download Best Model (.pkl)",
    data=model_bytes,
    file_name="best_model.pkl",
    mime="application/octet-stream",
    use_container_width=True
)

# ==========================================================
# PREDICTION FORM
# ==========================================================
st.divider()
st.subheader("🔮 Predict New Data")

feature_columns = st.session_state.get("feature_columns", [])

if feature_columns:

    input_data = {}

    for col in feature_columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            input_data[col] = st.number_input(
                f"{col}",
                value=float(df[col].median())
            )
        else:
            input_data[col] = st.selectbox(
                f"{col}",
                sorted(df[col].dropna().unique())
            )
    # ==========================================================
    # PREDICT BUTTON
    # ==========================================================
    if st.button("🔮 Predict", use_container_width=True):

        # Convert user inputs to DataFrame
        input_df = pd.DataFrame([input_data])

        # Load trained model
        model = st.session_state["trained_model"]

        # Make prediction
        try:
            prediction = model.predict(input_df)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            st.stop()

        st.divider()
        st.subheader("🎯 Prediction Result")

        if st.session_state["problem_type"] == "regression":
            st.success(f"Predicted {st.session_state['target_column']}: {prediction[0]:,.2f}")
        else:
            st.success(f"Predicted {st.session_state['target_column']}: {prediction[0]}")    