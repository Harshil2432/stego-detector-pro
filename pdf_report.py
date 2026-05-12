from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib import colors

from datetime import datetime

import os

# ============================================
# OUTPUT DIRECTORY
# ============================================

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# GENERATE PDF REPORT
# ============================================

def generate_pdf_report(file_path, results):

    # ============================================
    # TIMESTAMP
    # ============================================

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    filename_time = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    pdf_path = (
        f"{OUTPUT_DIR}/"
        f"forensic_report_{filename_time}.pdf"
    )

    # ============================================
    # CREATE PDF
    # ============================================

    doc = SimpleDocTemplate(
        pdf_path,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    elements = []

    # ============================================
    # TITLE
    # ============================================

    title = Paragraph(
        """
        <font size=24>
        <b>Advanced Digital Forensics Report</b>
        </font>
        """,
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # ============================================
    # RISK CLASSIFICATION
    # ============================================

    risk = "LOW"

    color = "green"

    if "HIGHLY SUSPICIOUS" in results:

        risk = "HIGH"

        color = "red"

    elif "POSSIBLY SUSPICIOUS" in results:

        risk = "MEDIUM"

        color = "orange"

    summary = Paragraph(
        f"""
        <font size=12>

        <b>Executive Summary</b><br/><br/>

        This forensic analysis was performed to
        identify possible hidden payloads,
        steganographic content, embedded files,
        metadata anomalies, suspicious binary
        patterns, and recursive hidden artifacts.

        <br/><br/>

        <b>Risk Level:</b>
        <font color='{color}'>
        <b>{risk}</b>
        </font>

        </font>
        """,
        styles['BodyText']
    )

    elements.append(summary)

    elements.append(Spacer(1, 20))

    # ============================================
    # FILE INFORMATION
    # ============================================

    try:

        file_size = (
            f"{os.path.getsize(file_path)} bytes"
        )

    except:

        file_size = "Unknown"

    info_data = [

        ["Scanned File", file_path],

        ["Generated Time", timestamp],

        ["File Size", file_size],

        ["Analysis Engine", "Advanced Stego Suite"],

        ["Scan Mode", "Deep Recursive Analysis"]

    ]

    table = Table(
        info_data,
        colWidths=[180, 320]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)

    ]))

    elements.append(table)

    elements.append(Spacer(1, 25))

    # ============================================
    # RESULTS HEADING
    # ============================================

    heading = Paragraph(
        """
        <font size=16>
        <b>Detailed Analysis Results</b>
        </font>
        """,
        styles['Heading2']
    )

    elements.append(heading)

    elements.append(Spacer(1, 12))

    # ============================================
    # FORMATTED RESULTS
    # ============================================

    formatted_results = results.replace(
        "\n",
        "<br/>"
    )

    result_paragraph = Paragraph(
        f"""
        <font face='Courier' size=8>
        {formatted_results}
        </font>
        """,
        styles['BodyText']
    )

    elements.append(result_paragraph)

    elements.append(Spacer(1, 20))

    # ============================================
    # FORENSIC NOTES
    # ============================================

    notes = Paragraph(
        """
        <font size=10>

        <b>Forensic Notes</b><br/><br/>

        • High entropy may indicate hidden or encrypted data.<br/>

        • Balanced LSB patterns may indicate
        LSB steganography techniques.<br/>

        • Embedded file signatures may reveal
        hidden payloads or recursive artifacts.<br/>

        • Metadata anomalies may indicate usage
        of online steganography tools.<br/>

        • Recursive analysis re-scans extracted
        hidden files automatically.

        </font>
        """,
        styles['BodyText']
    )

    elements.append(notes)

    elements.append(Spacer(1, 30))

    # ============================================
    # FOOTER
    # ============================================

    footer = Paragraph(
        """
        <font size=9 color='grey'>

        Generated by Advanced Digital
        Forensics & Steganography Analyzer

        </font>
        """,
        styles['BodyText']
    )

    elements.append(footer)

    # ============================================
    # BUILD PDF
    # ============================================

    doc.build(elements)

    return pdf_path