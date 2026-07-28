import pandas as pd


def generate_statistics(df):

    stats = {}

    numeric_df = df.select_dtypes(include="number")

    for column in numeric_df.columns:

        stats[column] = {
            "Mean": round(df[column].mean(), 2),
            "Median": round(df[column].median(), 2),
            "Minimum": round(df[column].min(), 2),
            "Maximum": round(df[column].max(), 2),
            "Std Dev": round(df[column].std(), 2)
        }

    return stats