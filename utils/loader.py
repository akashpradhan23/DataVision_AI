import pandas as pd


def load_dataset(uploaded_file):
    """
    Reads CSV or Excel file and returns a Pandas DataFrame.
    """

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    else:
        return None

    return df