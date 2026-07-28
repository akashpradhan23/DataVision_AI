import pandas as pd


def generate_report_metrics(df):

    rows = len(df)
    columns = len(df.columns)

    missing_values = int(df.isnull().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    numeric_columns = len(
        df.select_dtypes(include="number").columns
    )

    categorical_columns = len(
        df.select_dtypes(include="object").columns
    )

    boolean_columns = len(
        df.select_dtypes(include="bool").columns
    )

    return {
        "rows": rows,
        "columns": columns,
        "missing": missing_values,
        "duplicates": duplicate_rows,
        "numeric": numeric_columns,
        "categorical": categorical_columns,
        "boolean": boolean_columns
    }