import pandas as pd


def generate_basic_insights(df):
    """
    Generate statistical insights for numeric columns.
    """

    insights = []

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:

        insights.append({
            "column": column,
            "mean": round(df[column].mean(), 2),
            "median": round(df[column].median(), 2),
            "minimum": round(df[column].min(), 2),
            "maximum": round(df[column].max(), 2),
            "std": round(df[column].std(), 2)
        })

    return insights


def detect_outliers(df):
    """
    Detect outliers in numeric columns using the IQR method.
    """

    outlier_results = []

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_limit = Q1 - (1.5 * IQR)
        upper_limit = Q3 + (1.5 * IQR)

        outliers = df[
            (df[column] < lower_limit) |
            (df[column] > upper_limit)
        ]

        outlier_results.append({
            "column": column,
            "count": len(outliers),
            "rows": outliers
        })

    return outlier_results


def generate_correlation_insights(df):
    """
    Generate insights for strong positive and negative correlations.
    """

    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] < 2:
        return []

    corr_matrix = numeric_df.corr()

    insights = []

    columns = corr_matrix.columns

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):

            correlation = corr_matrix.iloc[i, j]

            # Show only strong correlations
            if abs(correlation) >= 0.7:

                if correlation > 0:
                    relation = "Strong Positive Correlation 📈"
                    explanation = (
                        f"As '{columns[i]}' increases, "
                        f"'{columns[j]}' also tends to increase."
                    )
                else:
                    relation = "Strong Negative Correlation 📉"
                    explanation = (
                        f"As '{columns[i]}' increases, "
                        f"'{columns[j]}' tends to decrease."
                    )

                insights.append({
                    "column1": columns[i],
                    "column2": columns[j],
                    "correlation": round(correlation, 2),
                    "relation": relation,
                    "explanation": explanation
                })

    return insights