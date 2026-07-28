def generate_dataset_summary(df):
    rows = df.shape[0]
    columns = df.shape[1]

    column_names = list(df.columns)

    data_types = df.dtypes.astype(str)

    missing_values = df.isnull().sum()

    sample_data = df.head(5)

    dataset_info = f"""
Dataset Shape:
Rows: {rows}
Columns: {columns}

Column Names:
{column_names}

Data Types:
{data_types.to_string()}

Missing Values:
{missing_values.to_string()}

Sample Data:
{sample_data.to_string()}
"""

    return dataset_info