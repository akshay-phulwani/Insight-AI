from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def _paragraph(text, style):
    return Paragraph(str(text), style)


def _dataframe_table(df, max_rows=20, max_columns=6):
    limited = df.head(max_rows).iloc[:, :max_columns].copy()
    limited = limited.fillna("")

    data = [limited.columns.tolist()] + limited.astype(str).values.tolist()

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    return table


def _key_value_table(items):
    data = [["Metric", "Value"]] + [[key, value] for key, value in items.items()]

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )

    return table


def _add_bullets(story, title, items, styles):
    story.append(Paragraph(title, styles["Heading2"]))

    for item in items:
        story.append(Paragraph(f"- {item}", styles["BodyText"]))

    story.append(Spacer(1, 12))


def generate_pdf_report(df, output_path, insights=None, dataset_name="Dataset"):
    styles = getSampleStyleSheet()
    story = []

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    total_missing = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())

    story.append(Paragraph("InsightAI Analytics Report", styles["Title"]))
    story.append(Paragraph(dataset_name, styles["Heading2"]))
    story.append(Spacer(1, 12))

    overview = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": total_missing,
        "Duplicate Rows": duplicate_rows,
    }

    story.append(Paragraph("Dataset Overview", styles["Heading2"]))
    story.append(_key_value_table(overview))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Summary Statistics", styles["Heading2"]))
    story.append(_dataframe_table(df.describe(include="all").reset_index()))
    story.append(Spacer(1, 14))

    missing = df.isnull().sum()
    missing_df = missing.reset_index()
    missing_df.columns = ["Column", "Missing Values"]

    story.append(Paragraph("Missing Values", styles["Heading2"]))
    story.append(_dataframe_table(missing_df, max_rows=50, max_columns=2))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Duplicate Rows", styles["Heading2"]))
    story.append(_key_value_table({"Duplicate Rows": duplicate_rows}))
    story.append(PageBreak())

    if insights:
        story.append(Paragraph("AI Insights", styles["Heading1"]))

        for section, items in insights.items():
            _add_bullets(story, section, items, styles)

    doc.build(story)

    return output_path
