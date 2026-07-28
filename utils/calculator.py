import pandas as pd


def calculate(df, operation, column):
    """
    Perform a calculation on a numeric column.
    """

    # Check if column exists
    if column not in df.columns:
        return "❌ Column not found."

    # Check if column is numeric
    if not pd.api.types.is_numeric_dtype(df[column]):
        return "❌ Selected column is not numeric."

    try:

        if operation == "mean":
            return round(df[column].mean(), 2)

        elif operation == "sum":
            return round(df[column].sum(), 2)

        elif operation == "max":
            return df[column].max()

        elif operation == "min":
            return df[column].min()

        elif operation == "count":
            return int(df[column].count())

        else:
            return "❌ Unsupported operation."

    except Exception as e:
        return f"❌ Error: {str(e)}"