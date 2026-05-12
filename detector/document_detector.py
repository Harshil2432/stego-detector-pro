from docx import Document
import PyPDF2

def scan_docx(file_path):
    doc = Document(file_path)
    hidden_text = []

    for para in doc.paragraphs:
        if para.text.strip() == "":
            continue

        # Detect suspicious invisible text
        if any(ord(c) < 32 for c in para.text):
            hidden_text.append(para.text)

    if hidden_text:
        return True, "[!] Suspicious hidden characters found in DOCX"
    else:
        return False, "[+] DOCX seems clean"


def scan_pdf(file_path):
    pdf = open(file_path, 'rb')
    reader = PyPDF2.PdfReader(pdf)

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    if "\x00" in text:
        return True, "[!] Suspicious encoding in PDF"
    
    return False, "[+] PDF seems clean"