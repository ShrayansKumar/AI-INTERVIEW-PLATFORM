from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)


def generate_report_pdf(final_report: dict, evaluations: list[dict]) -> bytes:
    """
    Generates a PDF version of the interview final report.
    Returns raw PDF bytes, ready to return from a FastAPI endpoint or save to disk.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"], fontSize=20, spaceAfter=6
    )
    heading_style = ParagraphStyle(
        "SectionHeading", parent=styles["Heading2"], spaceBefore=16, spaceAfter=8,
        textColor=colors.HexColor("#1a1a2e")
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=10, leading=14, spaceAfter=6
    )

    story = []

    # ── Header ──────────────────────────────────────────────────
    story.append(Paragraph("Interview Performance Report", title_style))
    story.append(Paragraph(f"Company: {final_report.get('company', 'N/A')}", body_style))
    story.append(Spacer(1, 12))

    # ── Candidate Summary ───────────────────────────────────────
    story.append(Paragraph("Candidate Summary", heading_style))
    summary = final_report.get("candidate_summary", {})
    skills_text = ", ".join(summary.get("top_skills", []))
    projects_text = ", ".join(summary.get("projects", []))
    story.append(Paragraph(f"<b>Top Skills:</b> {skills_text}", body_style))
    story.append(Paragraph(f"<b>Projects:</b> {projects_text}", body_style))

    # ── Interview Metrics Table ──────────────────────────────────
    story.append(Paragraph("Interview Metrics", heading_style))
    metrics = final_report.get("interview_metrics", {})
    metrics_data = [
        ["Metric", "Score"],
        ["Technical Accuracy", f"{metrics.get('average_technical_accuracy', 0)} / 10"],
        ["Communication", f"{metrics.get('average_communication', 0)} / 10"],
        ["Problem Solving", f"{metrics.get('average_problem_solving', 0)} / 10"],
        ["Depth", f"{metrics.get('average_depth', 0)} / 10"],
        ["Overall Score", f"{metrics.get('overall_score', 0)} / 10"],
    ]
    metrics_table = Table(metrics_data, colWidths=[3 * inch, 2 * inch])
    metrics_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f0f5")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 12))

    # ── Recommendation ───────────────────────────────────────────
    story.append(Paragraph("Recommendation", heading_style))
    story.append(Paragraph(final_report.get("recommendation", "N/A"), body_style))

    # ── Feedback ──────────────────────────────────────────────────
    feedback = final_report.get("feedback", {})

    story.append(Paragraph("Strengths", heading_style))
    for item in feedback.get("strengths", []):
        story.append(Paragraph(f"• {item}", body_style))

    story.append(Paragraph("Weaknesses", heading_style))
    for item in feedback.get("weaknesses", []):
        story.append(Paragraph(f"• {item}", body_style))

    story.append(Paragraph("Improvement Areas", heading_style))
    for item in feedback.get("improvement_areas", []):
        story.append(Paragraph(f"• {item}", body_style))

    # ── Detailed Q&A on a new page ───────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("Question-by-Question Breakdown", heading_style))

    for i, ev in enumerate(evaluations, 1):
        story.append(Paragraph(f"<b>Q{i}: {ev.get('question', '')}</b>", body_style))
        story.append(Paragraph(f"<i>Answer:</i> {ev.get('answer', '')}", body_style))
        story.append(Paragraph(
            f"Technical: {ev.get('technical_accuracy', 0)}/10 &nbsp;&nbsp; "
            f"Communication: {ev.get('communication', 0)}/10 &nbsp;&nbsp; "
            f"Problem Solving: {ev.get('problem_solving', 0)}/10 &nbsp;&nbsp; "
            f"Depth: {ev.get('depth', 0)}/10",
            body_style
        ))
        story.append(Paragraph(f"<i>{ev.get('summary', '')}</i>", body_style))
        story.append(Spacer(1, 10))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes