import pandas as pd

def clean_dataset(df):
    """
    Cleans the dataset and returns:
    - cleaned DataFrame
    - cleaning statistics
    """

    cleaned_df = df.copy()

    # Count values before cleaning
    duplicates_before = cleaned_df.duplicated().sum()
    missing_before = cleaned_df.isnull().sum().sum()

    # Remove duplicates
    cleaned_df = cleaned_df.drop_duplicates()

    # Fill numeric columns
    numeric_columns = cleaned_df.select_dtypes(include=["number"]).columns

    for column in numeric_columns:
        cleaned_df[column] = cleaned_df[column].fillna(
            cleaned_df[column].mean()
        )

    # Fill categorical columns
    categorical_columns = cleaned_df.select_dtypes(include=["object"]).columns

    for column in categorical_columns:
        if not cleaned_df[column].mode().empty:
            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].mode()[0]
            )

    # Count values after cleaning
    duplicates_after = cleaned_df.duplicated().sum()
    missing_after = cleaned_df.isnull().sum().sum()

    stats = {
        "duplicates_removed": duplicates_before - duplicates_after,
        "missing_values_filled": missing_before - missing_after
    }

    return cleaned_df, stats