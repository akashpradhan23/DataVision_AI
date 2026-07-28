import pandas as pd
import plotly.express as px

def get_column_summary(df):
    """
    Returns the count of different column types.
    """

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = df.select_dtypes(include=["object"]).columns.tolist()
    boolean_columns = df.select_dtypes(include=["bool"]).columns.tolist()
    datetime_columns = df.select_dtypes(include=["datetime"]).columns.tolist()

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "numeric": len(numeric_columns),
        "categorical": len(categorical_columns),
        "boolean": len(boolean_columns),
        "datetime": len(datetime_columns)
    }

    return summary


def create_histogram(df, column):
    """
    Creates an interactive histogram for the selected column.
    """

    fig = px.histogram(
        df,
        x=column,
        title=f"Distribution of {column}",
        nbins=20
    )

    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count"
    )

    return fig


def create_box_plot(df, column):
    """
    Creates an interactive box plot for the selected column.
    """

    fig = px.box(
        df,
        y=column,
        title=f"Box Plot of {column}"
    )

    fig.update_layout(
        yaxis_title=column
    )

    return fig

def create_scatter_plot(df, x_column, y_column):
    """
    Creates an interactive scatter plot.
    """

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"{y_column} vs {x_column}"
    )

    fig.update_layout(
        xaxis_title=x_column,
        yaxis_title=y_column
    )

    return fig

import plotly.express as px

def create_correlation_heatmap(df):
    """
    Creates an interactive correlation heatmap
    using all numeric columns.
    """

    numeric_df = df.select_dtypes(include=["number"])

    corr_matrix = numeric_df.corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap"
    )

    fig.update_layout(
        height=600
    )

    return fig

def get_categorical_columns(df):
    """
    Returns all categorical columns.
    """

    return df.select_dtypes(include=["object"]).columns.tolist()

def get_dashboard_metrics(df):
    """
    Returns basic dashboard metrics.
    """

    numeric_columns = df.select_dtypes(include=["number"]).columns

    metrics = {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_columns": len(numeric_columns),
        "categorical_columns": len(
            df.select_dtypes(include=["object"]).columns
        )
    }

    if len(numeric_columns) > 0:
        first_numeric = numeric_columns[0]

        metrics["average"] = round(df[first_numeric].mean(), 2)
        metrics["maximum"] = round(df[first_numeric].max(), 2)
    else:
        metrics["average"] = "-"
        metrics["maximum"] = "-"

    return metrics

def create_bar_chart(df, column):
    """
    Creates a bar chart showing the count of each category.
    """

    import plotly.express as px

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Count"]

    fig = px.bar(
        counts,
        x=column,
        y="Count",
        title=f"Bar Chart of {column}"
    )

    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count",
        template="plotly_white"
    )

    return fig

def create_pie_chart(df, column):
    """
    Creates a pie chart showing the proportion of each category.
    """

    import plotly.express as px

    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Count"]

    fig = px.pie(
        counts,
        names=column,
        values="Count",
        title=f"Pie Chart of {column}"
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig