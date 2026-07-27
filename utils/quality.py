import pandas as pd


def get_dataset_summary(df):

    """
    Returns basic information about the dataset.
    """

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": df.isnull().sum().sum(),
        "duplicate_rows": df.duplicated().sum(),
        "memory_usage": round(df.memory_usage(deep=True).sum() / (1024 ** 2), 2)
    }

    return summary
def get_missing_values(df):
    """
    Returns missing values count and percentage for each column.
    """

    missing = df.isnull().sum()

    percentage = (missing / len(df) * 100).round(2)

    result = missing.to_frame(name="Missing Values")

    result["Missing %"] = percentage

    result = result[result["Missing Values"] > 0]

    return result

def calculate_quality_score(df):
    """
    Calculates a simple data quality score out of 100.
    """

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    score = 100 - missing - (duplicates * 2)

    score = max(score, 0)

    return score