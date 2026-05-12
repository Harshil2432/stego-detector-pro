# ============================================
# 🔐 DIGITAL FORENSICS STEGO SUITE
# Full Working GUI + PDF Report Version
# ============================================

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from universal_extractor import analyze_file

import io
import sys
import threading
import os

# PDF REPORT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

# ============================================
# 📂 OUTPUT DIRECTORY
# ============================================

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# 🌍 GLOBAL VARIABLES
# ============================================

last_results = ""
last_file = ""

# ============================================
# 📄 PDF REPORT GENERATOR
# ============================================

def generate_pdf_report(file_path, results):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    pdf_path = (
        f"{OUTPUT_DIR}/forensic_report_{timestamp}.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    elements = []

    # TITLE
    title = Paragraph(
        "Digital Forensics Steganography Report",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # FILE INFO
    info_data = [
        ["File Path", file_path],
        ["Generated", timestamp]
    ]

    table = Table(
        info_data,
        colWidths=[150, 350]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # RESULTS
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

    # BUILD PDF
    doc.build(elements)

    return pdf_path


# ============================================
# 🖥️ UPDATE OUTPUT BOX
# ============================================

def update_output(results):

    output.insert(tk.END, results)

    output.see(tk.END)

    root.update_idletasks()


# ============================================
# 🧠 RUN FORENSIC ANALYSIS
# ============================================

def run_analysis(file_path):

    global last_results
    global last_file

    # Capture console output
    captured_output = io.StringIO()

    sys.stdout = captured_output

    try:
        analyze_file(file_path)

    except Exception as e:
        print("[ERROR]", e)

    finally:
        sys.stdout = sys.__stdout__

    # Get results
    results = captured_output.getvalue()

    results += "\n\n✅ FORENSIC SCAN FINISHED\n"

    # Save globally
    last_results = results
    last_file = file_path

    # Update GUI
    output.after(
        0,
        lambda: update_output(results)
    )


# ============================================
# 🔍 FILE SCAN
# ============================================

def scan_file():

    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    output.delete(1.0, tk.END)

    output.insert(
        tk.END,
        f"🔍 Scanning:\n{file_path}\n\n"
    )

    # Thread
    thread = threading.Thread(
        target=run_analysis,
        args=(file_path,)
    )

    thread.daemon = True

    thread.start()


# ============================================
# 📄 SAVE PDF REPORT
# ============================================

def save_pdf():

    global last_results
    global last_file

    if not last_results:

        messagebox.showwarning(
            "No Results",
            "Please scan a file first."
        )

        return

    try:

        pdf_path = generate_pdf_report(
            last_file,
            last_results
        )

        output.insert(
            tk.END,
            f"\n📄 PDF Report Saved:\n{pdf_path}\n"
        )

        messagebox.showinfo(
            "Saved",
            f"PDF Report Saved:\n{pdf_path}"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# ============================================
# 🖥️ MAIN GUI
# ============================================

root = tk.Tk()

root.title(
    "🔐 Digital Forensics Stego Suite"
)

root.geometry("1000x700")

# ============================================
# TITLE
# ============================================

title = tk.Label(
    root,
    text=(
        "🔐 Digital Forensics & "
        "Steganography Analyzer"
    ),
    font=("Arial", 18, "bold")
)

title.pack(pady=10)

# ============================================
# BUTTON FRAME
# ============================================

button_frame = tk.Frame(root)

button_frame.pack(pady=10)

# ============================================
# SCAN BUTTON
# ============================================

scan_btn = tk.Button(
    button_frame,
    text="Select File & Scan",
    command=scan_file,
    width=25,
    height=2,
    bg="black",
    fg="white",
    font=("Arial", 11, "bold")
)

scan_btn.grid(
    row=0,
    column=0,
    padx=10
)

# ============================================
# PDF BUTTON
# ============================================

pdf_btn = tk.Button(
    button_frame,
    text="Save PDF Report",
    command=save_pdf,
    width=25,
    height=2,
    bg="darkred",
    fg="white",
    font=("Arial", 11, "bold")
)

pdf_btn.grid(
    row=0,
    column=1,
    padx=10
)

# ============================================
# OUTPUT TEXT BOX
# ============================================

output = tk.Text(
    root,
    wrap="word",
    font=("Consolas", 10)
)

output.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# ============================================
# START GUI
# ============================================

root.mainloop()