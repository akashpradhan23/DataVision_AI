def get_question_type(question):

    question = question.lower()

    words = question.split()

    calculation_keywords = [
        "average",
        "mean",
        "sum",
        "total",
        "count",
        "maximum",
        "minimum",
        "highest",
        "lowest",
        "top",
        "max",
        "min"
    ]

    for word in words:
        if word in calculation_keywords:
            return "calculation"

    return "general"