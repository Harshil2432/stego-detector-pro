import os
import base64
from PIL import Image
import numpy as np
from stegano import lsb
import PyPDF2
from docx import Document

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===================================
# 🔓 IMAGE EXTRACTION
# ===================================
def extract_from_image(file_path):

    print("\n[IMAGE ANALYSIS]")

    # LSB extraction
    try:
        msg = lsb.reveal(file_path)

        if msg:
            print("[🚨] Hidden LSB Message Found:")
            print(msg)
        else:
            print("[+] No LSB hidden message found")

    except Exception:
        print("[!] LSB extraction failed")

    # Image load
    try:
        img = Image.open(file_path)
        pixels = np.array(img)

        print("[+] Image loaded successfully")
        print(f"[+] Shape: {pixels.shape}")

    except Exception as e:
        print("[!] Image analysis failed:", e)


# ===================================
# 📄 DOCUMENT EXTRACTION
# ===================================
def extract_from_doc(file_path):

    print("\n[DOCUMENT ANALYSIS]")

    if file_path.endswith(".pdf"):

        try:
            reader = PyPDF2.PdfReader(file_path)

            for page in reader.pages:

                text = page.extract_text()

                if text:
                    print("[+] Extracted PDF Text:")
                    print(text[:500])

        except Exception:
            print("[!] PDF extraction failed")

    elif file_path.endswith(".docx"):

        try:
            doc = Document(file_path)

            for para in doc.paragraphs:
                print("[+]", para.text)

        except Exception:
            print("[!] DOCX extraction failed")


# ===================================
# 🔍 STRINGS EXTRACTION
# ===================================
def extract_strings(file_path):

    print("\n[STRINGS ANALYSIS]")

    try:
        with open(file_path, "rb") as f:
            data = f.read()

        strings = []
        current = ""

        for byte in data:

            if 32 <= byte <= 126:
                current += chr(byte)

            else:
                if len(current) > 5:
                    strings.append(current)

                current = ""

        print("[+] Found Strings:")

        for s in strings[:30]:
            print("   ", s)

    except Exception as e:
        print("[!] Strings extraction failed:", e)


# ===================================
# 🔬 DEEP SCAN
# ===================================
def deep_scan(file_path):

    print("\n[DEEP SCAN]")

    try:
        with open(file_path, "rb") as f:
            data = f.read()

        # HEX preview
        print("[+] HEX Preview:")
        print(data[:64].hex())

        # Readable preview
        printable = ''.join(
            chr(b) if 32 <= b <= 126 else '.'
            for b in data[:300]
        )

        print("\n[+] Readable Preview:")
        print(printable)

        # Keywords
        keywords = [
            b"flag",
            b"ctf",
            b"password",
            b"secret",
            b"key"
        ]

        for k in keywords:

            if k in data.lower():
                print(f"[🚨] Keyword detected: {k.decode()}")

        # Base64 detection
        try:
            decoded = base64.b64decode(
                data[:200],
                validate=True
            )

            if decoded:
                print("[!] Possible Base64 encoded content detected")

        except:
            pass

    except Exception as e:
        print("[!] Deep scan failed:", e)


# ===================================
# 📦 FILE CARVING
# ===================================
def carve_files(file_path):

    print("\n[FILE CARVING]")

    extracted_files = []

    try:
        with open(file_path, "rb") as f:
            data = f.read()

        signatures = {
            b"\x89PNG": "png",
            b"%PDF": "pdf",
            b"PK\x03\x04": "zip",
            b"\xFF\xD8\xFF": "jpg"
        }

        for sig, ext in signatures.items():

            positions = []
            start = 0

            while True:

                pos = data.find(sig, start)

                if pos == -1:
                    break

                positions.append(pos)
                start = pos + 1

            # Ignore first signature
            if len(positions) > 1:

                for i, pos in enumerate(positions[1:], start=1):

                    extracted_path = f"output/extracted_{i}.{ext}"

                    with open(extracted_path, "wb") as out:
                        out.write(data[pos:])

                    extracted_files.append(extracted_path)

                    print(f"[🚨] Embedded {ext.upper()} extracted:")
                    print(f"    → {extracted_path}")

            else:
                print(f"[+] No embedded {ext.upper()} detected")

    except Exception as e:
        print("[!] File carving failed:", e)

    return extracted_files


# ===================================
# 🔁 RECURSIVE ANALYSIS
# ===================================
def recursive_scan(extracted_files):

    print("\n[RECURSIVE SCAN]")

    if not extracted_files:
        print("[+] No extracted files to analyze")
        return

    for path in extracted_files:

        if os.path.isfile(path):

            print(f"\n🔁 Re-analyzing extracted file: {path}")

            analyze_file(path, recursive=False)


# ===================================
# 🎯 MAIN ANALYZER
# ===================================
def analyze_file(file_path, recursive=True):

    print("\n==============================")
    print("🔍 ANALYZING FILE:", file_path)
    print("==============================")

    if not os.path.exists(file_path):
        print("[ERROR] File not found")
        return

    # =========================
    # IMAGE
    # =========================
    if file_path.endswith((".png", ".jpg", ".jpeg")):
        extract_from_image(file_path)

    # =========================
    # DOCUMENTS
    # =========================
    elif file_path.endswith((".pdf", ".docx")):
        extract_from_doc(file_path)

    # =========================
    # GENERIC ANALYSIS
    # =========================
    extract_strings(file_path)

    deep_scan(file_path)

    # =========================
    # FILE CARVING
    # =========================
    extracted_files = carve_files(file_path)

    # =========================
    # RECURSIVE SCAN
    # =========================
    if recursive:
        recursive_scan(extracted_files)

    print("\n✅ Analysis Completed")


# ===================================
# ▶️ RUN
# ===================================
if __name__ == "__main__":

    path = input("Enter file path: ")

    analyze_file(path)