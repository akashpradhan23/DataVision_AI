import re


def extract_intent(question, columns):
    """
    Extract operation and column from the user's question.
    """

    question = question.lower()

    # Remove punctuation (?, . , ! etc.)
    question = re.sub(r"[^\w\s]", "", question)

    # ---------------- Operation ---------------- #

    operation = None

    if "average" in question or "mean" in question:
        operation = "mean"

    elif "sum" in question or "total" in question:
        operation = "sum"

    elif "maximum" in question or "highest" in question or "max" in question:
        operation = "max"

    elif "minimum" in question or "lowest" in question or "min" in question:
        operation = "min"

    elif "count" in question:
        operation = "count"

    # ---------------- Column ---------------- #

    column = None

    words = question.split()

    for col in columns:

        cleaned_column = col.lower().replace("_", " ")

        if cleaned_column in question:
            column = col
            break

        col_words = cleaned_column.split()

        if any(word in col_words for word in words):
            column = col
            break

    return operation, column