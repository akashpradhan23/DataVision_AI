import plotly.express as px


def create_chart(analysis):

    if analysis.get("analysis_type") != "groupby":
        return None

    df = analysis["table"].reset_index()

    x = df.columns[0]
    y = df.columns[1]

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=f"{y} by {x}",
        text_auto=True
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title=x,
        yaxis_title=y
    )

    return fig