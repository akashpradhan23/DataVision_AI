import plotly.express as px


def generate_dashboard(df):

    charts = {}

    # Revenue by City
    if "City" in df.columns and "Total_Amount" in df.columns:

        city_df = (
            df.groupby("City")["Total_Amount"]
            .sum()
            .reset_index()
        )

        charts["Revenue by City"] = px.bar(
            city_df,
            x="City",
            y="Total_Amount",
            title="Revenue by City"
        )

    # Sales by Region
    if "Region" in df.columns and "Total_Amount" in df.columns:

        region_df = (
            df.groupby("Region")["Total_Amount"]
            .sum()
            .reset_index()
        )

        charts["Revenue by Region"] = px.pie(
            region_df,
            names="Region",
            values="Total_Amount",
            title="Revenue by Region"
        )

    # Customer Age Distribution
    if "Customer_Age" in df.columns:

        charts["Customer Age Distribution"] = px.histogram(
            df,
            x="Customer_Age",
            nbins=20,
            title="Customer Age Distribution"
        )

    # Product Revenue
    if "Product" in df.columns and "Total_Amount" in df.columns:

        product_df = (
            df.groupby("Product")["Total_Amount"]
            .sum()
            .reset_index()
        )

        charts["Revenue by Product"] = px.bar(
            product_df,
            x="Product",
            y="Total_Amount",
            title="Revenue by Product"
        )

    return charts