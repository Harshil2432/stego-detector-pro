from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import Table
from reportlab.platypus.tables import TableStyle
from reportlab.lib import colors
import os
from datetime import datetime

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_pdf_report(file_path, results):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    pdf_path = f"{OUTPUT_DIR}/forensic_report_{timestamp}.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    # =========================
    # TITLE
    # =========================
    title = Paragraph(
        "Digital Forensics Steganography Report",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # =========================
    # FILE INFO
    # =========================
    info_data = [
        ["File Path", file_path],
        ["Generated", timestamp]
    ]

    table = Table(info_data, colWidths=[150, 350])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # =========================
    # RESULTS
    # =========================
    result_title = Paragraph(
        "<b>Analysis Results</b>",
        styles['Heading2']
    )

    elements.append(result_title)

    result_para = Paragraph(
        results.replace("\n", "<br/>"),
        styles['BodyText']
    )

    elements.append(result_para)

    # =========================
    # BUILD PDF
    # =========================
    doc.build(elements)

    return pdf_path