from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor

import os


def generate_pdf(filename, title, report, chart_path=None):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#1F4E79")

    heading_style = styles["Heading2"]
    heading_style.textColor = HexColor("#1F4E79")

    normal = styles["BodyText"]

    story = []

    # -----------------------------------------
    # Cover Title
    # -----------------------------------------
    story.append(
        Paragraph(title, title_style)
    )

    story.append(Spacer(1, 20))

    # -----------------------------------------
    # Report Sections
    # -----------------------------------------
    lines = report.split("\n")

    headings = [
        "Executive Summary",
        "Dataset Overview",
        "Data Quality",
        "Key Findings",
        "Business Insights",
        "Recommendations",
        "Conclusion"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        if line in headings:

            story.append(
                Paragraph(line, heading_style)
            )

            story.append(Spacer(1, 8))

        else:

            story.append(
                Paragraph(line, normal)
            )

            story.append(Spacer(1, 5))

    # -----------------------------------------
    # Add Chart
    # -----------------------------------------
    if chart_path and os.path.exists(chart_path):

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "Visualization",
                heading_style
            )
        )

        story.append(Spacer(1, 10))

        story.append(
            Image(
                chart_path,
                width=450,
                height=270
            )
        )

    doc.build(story)