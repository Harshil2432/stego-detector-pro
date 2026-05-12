import os
import base64
import math

from PIL import Image
import numpy as np

from stegano import lsb

import PyPDF2
from docx import Document

from scipy.stats import chisquare

import exifread

# ===================================
# OUTPUT DIRECTORY
# ===================================
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===================================
# ADVANCED IMAGE ANALYSIS
# ===================================
def extract_from_image(file_path):

    print("\n[ADVANCED IMAGE ANALYSIS]")

    suspicious_score = 0

    # ===================================
    # IMAGE LOAD
    # ===================================
    try:
        img = Image.open(file_path)

        pixels = np.array(img)

        print("[+] Image loaded successfully")
        print(f"[+] Shape: {pixels.shape}")

    except Exception as e:
        print("[!] Image load failed:", e)
        return

    # ===================================
    # LSB EXTRACTION
    # ===================================
    try:
        hidden_msg = lsb.reveal(file_path)

        if hidden_msg:

            print("[🚨] Hidden LSB Message Found:")
            print(hidden_msg)

            suspicious_score += 40

        else:
            print("[+] No direct hidden message found")

    except Exception:
        print("[!] LSB extraction failed")

    # ===================================
    # ENTROPY ANALYSIS
    # ===================================
    try:
        hist, _ = np.histogram(
            pixels.flatten(),
            bins=256
        )

        hist = hist / hist.sum()

        entropy = -sum(
            p * math.log2(p)
            for p in hist
            if p > 0
        )

        print(f"[+] Entropy: {entropy:.4f}")

        if entropy > 7.3:

            print("[🚨] High entropy detected")

            suspicious_score += 20

    except Exception as e:
        print("[!] Entropy analysis failed:", e)

    # ===================================
    # LSB DISTRIBUTION
    # ===================================
    try:
        lsb_bits = pixels & 1

        unique, counts = np.unique(
            lsb_bits,
            return_counts=True
        )

        lsb_dict = {
            int(k): int(v)
            for k, v in zip(unique, counts)
        }

        print("[+] LSB Distribution:", lsb_dict)

        count_0 = lsb_dict.get(0, 0)
        count_1 = lsb_dict.get(1, 0)

        total = count_0 + count_1

        balance = abs(count_0 - count_1) / total

        print(f"[+] LSB Balance: {balance:.4f}")

        if balance < 0.05:

            print("[🚨] Suspicious LSB balancing")

            suspicious_score += 20

    except Exception as e:
        print("[!] LSB analysis failed:", e)

    # ===================================
    # CHI-SQUARE TEST
    # ===================================
    try:
        observed = [count_0, count_1]

        expected = [total / 2, total / 2]

        chi, p = chisquare(
            observed,
            expected
        )

        print(f"[+] Chi-Square p-value: {p:.6f}")

        if p > 0.85:

            print("[🚨] Statistical anomaly detected")

            suspicious_score += 15

    except Exception as e:
        print("[!] Chi-square analysis failed:", e)

    # ===================================
    # METADATA ANALYSIS
    # ===================================
    try:
        with open(file_path, "rb") as f:

            tags = exifread.process_file(f)

        if tags:

            print("[+] Metadata found")

            suspicious_keywords = [
                "steg",
                "hidden",
                "secret",
                "encoder"
            ]

            for tag in tags:

                value = str(tags[tag]).lower()

                for keyword in suspicious_keywords:

                    if keyword in value:

                        print(
                            f"[🚨] Suspicious metadata: {value}"
                        )

                        suspicious_score += 10

        else:
            print("[+] No metadata found")

    except Exception as e:
        print("[!] Metadata analysis failed:", e)

    # ===================================
    # FINAL VERDICT
    # ===================================
    print(f"\n[+] Suspicion Score: {suspicious_score}/100")

    if suspicious_score >= 60:

        print("🚨 HIGHLY SUSPICIOUS IMAGE")

    elif suspicious_score >= 30:

        print("⚠ POSSIBLY SUSPICIOUS IMAGE")

    else:

        print("✅ LIKELY CLEAN IMAGE")


# ===================================
# DOCUMENT ANALYSIS
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

            suspicious_chars = [
                '\u200b',
                '\u200c',
                '\u200d'
            ]

            for para in doc.paragraphs:

                print("[+]", para.text)

                if any(
                    c in para.text
                    for c in suspicious_chars
                ):

                    print(
                        "[🚨] Hidden Unicode characters detected"
                    )

        except Exception:
            print("[!] DOCX extraction failed")


# ===================================
# STRINGS EXTRACTION
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

                if len(current) > 7:

                    strings.append(current)

                current = ""

        print("[+] Found Strings:")

        for s in strings[:30]:

            print("   ", s)

    except Exception as e:
        print("[!] Strings extraction failed:", e)


# ===================================
# DEEP SCAN
# ===================================
def deep_scan(file_path):

    print("\n[DEEP SCAN]")

    try:
        with open(file_path, "rb") as f:

            data = f.read()

        # ===================================
        # HEX PREVIEW
        # ===================================
        print("[+] HEX Preview:")

        print(data[:64].hex())

        # ===================================
        # READABLE PREVIEW
        # ===================================
        printable = ''.join(
            chr(b) if 32 <= b <= 126 else '.'
            for b in data[:300]
        )

        print("\n[+] Readable Preview:")

        print(printable)

        # ===================================
        # KEYWORD DETECTION
        # ===================================
        keywords = [
            b"flag",
            b"ctf",
            b"password",
            b"secret",
            b"key",
            b"token",
            b"apikey",
            b"hidden",
            b"encrypt"
        ]

        for k in keywords:

            if k in data.lower():

                print(
                    f"[🚨] Keyword detected: {k.decode()}"
                )

        # ===================================
        # BASE64 DETECTION
        # ===================================
        try:
            decoded = base64.b64decode(
                data[:200],
                validate=True
            )

            if decoded:

                print(
                    "[🚨] Possible Base64 encoded content detected"
                )

        except:
            pass

    except Exception as e:
        print("[!] Deep scan failed:", e)


# ===================================
# FILE CARVING
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
            b"\xFF\xD8\xFF": "jpg",
            b"GIF89a": "gif",
            b"RIFF": "wav"
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

            # Ignore original file header
            if len(positions) > 1:

                for i, pos in enumerate(
                    positions[1:],
                    start=1
                ):

                    extracted_path = (
                        f"{OUTPUT_DIR}/extracted_{i}.{ext}"
                    )

                    with open(
                        extracted_path,
                        "wb"
                    ) as out:

                        out.write(data[pos:])

                    extracted_files.append(
                        extracted_path
                    )

                    print(
                        f"[🚨] Embedded {ext.upper()} extracted:"
                    )

                    print(
                        f"    → {extracted_path}"
                    )

            else:

                print(
                    f"[+] No embedded {ext.upper()} detected"
                )

    except Exception as e:
        print("[!] File carving failed:", e)

    return extracted_files


# ===================================
# RECURSIVE ANALYSIS
# ===================================
def recursive_scan(extracted_files):

    print("\n[RECURSIVE SCAN]")

    if not extracted_files:

        print("[+] No extracted files to analyze")

        return

    for path in extracted_files:

        if os.path.isfile(path):

            print(
                f"\n🔁 Re-analyzing extracted file: {path}"
            )

            analyze_file(
                path,
                recursive=False
            )


# ===================================
# MAIN ANALYZER
# ===================================
def analyze_file(file_path, recursive=True):

    print("\n==============================")

    print("🔍 ANALYZING FILE:", file_path)

    print("==============================")

    if not os.path.exists(file_path):

        print("[ERROR] File not found")

        return

    # ===================================
    # IMAGE ANALYSIS
    # ===================================
    if file_path.endswith(
        (".png", ".jpg", ".jpeg")
    ):

        extract_from_image(file_path)

    # ===================================
    # DOCUMENT ANALYSIS
    # ===================================
    elif file_path.endswith(
        (".pdf", ".docx")
    ):

        extract_from_doc(file_path)

    # ===================================
    # GENERIC ANALYSIS
    # ===================================
    extract_strings(file_path)

    deep_scan(file_path)

    # ===================================
    # FILE CARVING
    # ===================================
    extracted_files = carve_files(file_path)

    # ===================================
    # RECURSIVE SCAN
    # ===================================
    if recursive:

        recursive_scan(extracted_files)

    print("\n✅ Analysis Completed")


# ===================================
# RUN PROGRAM
# ===================================
if __name__ == "__main__":

    path = input("Enter file path: ")

    analyze_file(path)