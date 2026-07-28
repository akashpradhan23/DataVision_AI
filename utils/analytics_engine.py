import pandas as pd


def run_analysis(
    df,
    analysis_type,
    operation,
    value_column,
    group_by="",
    ranking=""
):
    """
    Execute analytical operations on a dataframe.
    """

    # ===========================================
    # SIMPLE ANALYSIS
    # ===========================================
    if analysis_type == "simple":

        if value_column not in df.columns:
            return {"error": "Column not found."}

        if not pd.api.types.is_numeric_dtype(df[value_column]):
            return {"error": "Selected column is not numeric."}

        if operation == "mean":
            value = round(df[value_column].mean(), 2)

        elif operation == "sum":
            value = round(df[value_column].sum(), 2)

        elif operation == "max":
            value = df[value_column].max()

        elif operation == "min":
            value = df[value_column].min()

        elif operation == "count":
            value = int(df[value_column].count())

        else:
            return {"error": "Unsupported operation."}

        return {
            "analysis_type": "simple",
            "operation": operation,
            "column": value_column,
            "result": value
        }

    # ===========================================
    # GROUP BY ANALYSIS
    # ===========================================
    elif analysis_type == "groupby":

        if group_by not in df.columns:
            return {"error": "Group column not found."}

        if value_column not in df.columns:
            return {"error": "Value column not found."}

        if not pd.api.types.is_numeric_dtype(df[value_column]):
            return {"error": "Value column is not numeric."}

        # Select aggregation
        if operation == "sum":
            grouped = df.groupby(group_by)[value_column].sum()

        elif operation == "mean":
            grouped = df.groupby(group_by)[value_column].mean()

        elif operation == "count":
            grouped = df.groupby(group_by)[value_column].count()

        elif operation == "max":
            grouped = df.groupby(group_by)[value_column].max()

        elif operation == "min":
            grouped = df.groupby(group_by)[value_column].min()

        else:
            return {"error": "Unsupported operation."}

        # Ranking
        if ranking == "highest":

            best_group = grouped.idxmax()
            best_value = grouped.max()

        elif ranking == "lowest":

            best_group = grouped.idxmin()
            best_value = grouped.min()

        else:

            best_group = None
            best_value = None

        return {
            "analysis_type": "groupby",
            "operation": operation,
            "group_by": group_by,
            "value_column": value_column,
            "best_group": best_group,
            "best_value": best_value,
            "table": grouped.sort_values(ascending=False)
        }

    return {"error": "Unsupported analysis type."}