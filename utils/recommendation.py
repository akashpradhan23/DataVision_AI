import pandas as pd


def recommend_visualizations(df):
    """
    Analyze the dataset and recommend suitable visualizations.
    """

    recommendations = []

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()

    # Histogram
    if len(numeric_columns) >= 1:
        recommendations.append({
            "chart": "📊 Histogram",
            "reason": "Numeric columns detected."
        })

    # Box Plot
    if len(numeric_columns) >= 1:
        recommendations.append({
            "chart": "📦 Box Plot",
            "reason": "Useful for detecting outliers."
        })

    # Scatter Plot
    if len(numeric_columns) >= 2:
        recommendations.append({
            "chart": "📈 Scatter Plot",
            "reason": "Multiple numeric columns available."
        })

    # Heatmap
    if len(numeric_columns) >= 2:
        recommendations.append({
            "chart": "🔥 Correlation Heatmap",
            "reason": "Shows relationships between numeric columns."
        })

    # Bar Chart
    if len(categorical_columns) >= 1:
        recommendations.append({
            "chart": "📊 Bar Chart",
            "reason": "Categorical columns detected."
        })

    # Pie Chart
    if len(categorical_columns) >= 1:
        recommendations.append({
            "chart": "🥧 Pie Chart",
            "reason": "Good for category proportions."
        })

    return recommendations