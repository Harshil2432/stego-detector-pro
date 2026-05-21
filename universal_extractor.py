# ============================================
# ADVANCED UNIVERSAL FORENSIC EXTRACTOR
# ============================================

import os
import math
import base64

from PIL import Image

import numpy as np

from stegano import lsb

import PyPDF2

from docx import Document

from scipy.stats import chisquare

import exifread

# ============================================
# OUTPUT DIRECTORY
# ============================================

OUTPUT_DIR = "output"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ============================================
# FILE INFO
# ============================================

def print_file_info(file_path):

    print("\n[FILE INFORMATION]")

    try:

        size = os.path.getsize(
            file_path
        )

        print(
            f"[+] File Name: "
            f"{os.path.basename(file_path)}"
        )

        print(
            f"[+] File Size: "
            f"{size} bytes"
        )

        print(
            f"[+] File Type: "
            f"{os.path.splitext(file_path)[1]}"
        )

    except Exception as e:

        print(
            "[ERROR] File info failed:"
        )

        print(e)

# ============================================
# IMAGE ANALYSIS
# ============================================

def extract_from_image(file_path):

    print("\n[ADVANCED IMAGE ANALYSIS]")

    suspicious_score = 0

    hidden_msg = None

    # ============================================
    # LOAD IMAGE
    # ============================================

    try:

        img = Image.open(file_path)

        pixels = np.array(img)

        print(
            "[+] Image loaded successfully"
        )

        print(
            f"[+] Shape: {pixels.shape}"
        )

    except Exception as e:

        print(
            "[ERROR] Image load failed:"
        )

        print(e)

        return

    # ============================================
    # LSB EXTRACTION
    # ============================================

    try:

        hidden_msg = lsb.reveal(
            file_path
        )

        if hidden_msg:

            print(
                "\n[🚨] Hidden LSB Message Found:"
            )

            print(hidden_msg[:500])

            if len(hidden_msg) > 500:

                print(
                    "\n[+] Payload truncated..."
                )

            suspicious_score += 50

        else:

            print(
                "[+] No hidden payload detected"
            )

    except Exception:

        print(
            "[!] LSB extraction failed"
        )

    # ============================================
    # ENTROPY ANALYSIS
    # ============================================

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

        print(
            f"[+] Entropy: {entropy:.4f}"
        )

        # ============================================
        # ENTROPY SCORING
        # ============================================

        if entropy > 7.0:

            print(
                "[🚨] Extremely high entropy"
            )

            suspicious_score += 30

        elif entropy > 6.0:

            print(
                "[⚠] Elevated entropy"
            )

            suspicious_score += 20

        elif entropy > 5.2:

            suspicious_score += 10

    except Exception as e:

        print(
            "[ERROR] Entropy failed:"
        )

        print(e)

    # ============================================
    # LSB ANALYSIS
    # ============================================

    try:

        lsb_bits = pixels & 1

        unique, counts = np.unique(
            lsb_bits,
            return_counts=True
        )

        lsb_dict = {

            int(k): int(v)

            for k, v in zip(
                unique,
                counts
            )

        }

        print(
            f"[+] LSB Distribution: "
            f"{lsb_dict}"
        )

        count_0 = lsb_dict.get(0, 0)

        count_1 = lsb_dict.get(1, 0)

        total = count_0 + count_1

        balance = abs(
            count_0 - count_1
        ) / total

        print(
            f"[+] LSB Balance: "
            f"{balance:.4f}"
        )

        # ============================================
        # BALANCE SCORING
        # ============================================

        if balance < 0.05:

            print(
                "[🚨] Highly suspicious "
                "LSB balancing"
            )

            suspicious_score += 30

        elif balance < 0.10:

            print(
                "[⚠] Suspicious "
                "LSB balancing"
            )

            suspicious_score += 20

        elif balance < 0.15:

            suspicious_score += 10

    except Exception as e:

        print(
            "[ERROR] LSB analysis failed:"
        )

        print(e)

    # ============================================
    # CHI-SQUARE TEST
    # ============================================

    try:

        observed = [
            count_0,
            count_1
        ]

        expected = [
            total / 2,
            total / 2
        ]

        chi, p_value = chisquare(
            observed,
            expected
        )

        print(
            f"[+] Chi-Square p-value: "
            f"{p_value:.6f}"
        )

        if p_value > 0.90:

            print(
                "[🚨] Strong statistical anomaly"
            )

            suspicious_score += 20

        elif p_value > 0.70:

            print(
                "[⚠] Moderate statistical anomaly"
            )

            suspicious_score += 10

    except Exception as e:

        print(
            "[ERROR] Chi-square failed:"
        )

        print(e)

    # ============================================
    # METADATA ANALYSIS
    # ============================================

    try:

        with open(file_path, "rb") as f:

            tags = exifread.process_file(f)

        if tags:

            print("[+] Metadata found")

            suspicious_keywords = [

                "steg",
                "hidden",
                "secret",
                "encoder",
                "openstego"

            ]

            for tag in tags:

                value = str(
                    tags[tag]
                ).lower()

                for keyword in suspicious_keywords:

                    if keyword in value:

                        print(
                            f"[🚨] Suspicious "
                            f"metadata: {value}"
                        )

                        suspicious_score += 10

        else:

            print(
                "[+] No metadata found"
            )

    except Exception as e:

        print(
            "[ERROR] Metadata failed:"
        )

        print(e)

    # ============================================
    # FINAL SCORE
    # ============================================

    suspicious_score = min(
        suspicious_score,
        100
    )

    print(
        f"\n[+] Suspicion Score: "
        f"{suspicious_score}/100"
    )

    # ============================================
    # FINAL VERDICT
    # ============================================

    if suspicious_score >= 70:

        print(
            "🚨 HIGHLY SUSPICIOUS IMAGE"
        )

    elif suspicious_score >= 40:

        print(
            "⚠ POSSIBLY SUSPICIOUS IMAGE"
        )

    else:

        print(
            "✅ LIKELY CLEAN IMAGE"
        )

# ============================================
# DOCUMENT ANALYSIS
# ============================================

def extract_from_doc(file_path):

    print("\n[DOCUMENT ANALYSIS]")

    try:

        if file_path.endswith(".pdf"):

            reader = PyPDF2.PdfReader(
                file_path
            )

            for page in reader.pages:

                text = page.extract_text()

                if text:

                    print(
                        "[+] Extracted PDF Text:"
                    )

                    print(text[:500])

        elif file_path.endswith(".docx"):

            doc = Document(file_path)

            for para in doc.paragraphs:

                print("[+]", para.text)

    except Exception as e:

        print(
            "[ERROR] Document analysis failed:"
        )

        print(e)

# ============================================
# STRING EXTRACTION
# ============================================

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

                if len(current) > 6:

                    strings.append(current)

                current = ""

        if strings:

            print("[+] Found Strings:")

            for s in strings[:20]:

                print("   ", s)

        else:

            print(
                "[+] No readable strings found"
            )

    except Exception as e:

        print(
            "[ERROR] String extraction failed:"
        )

        print(e)

# ============================================
# DEEP SCAN
# ============================================

def deep_scan(file_path):

    print("\n[DEEP SCAN]")

    try:

        with open(file_path, "rb") as f:

            data = f.read()

        print("[+] HEX Preview:")

        print(data[:64].hex())

        printable = ''.join(

            chr(b)

            if 32 <= b <= 126

            else '.'

            for b in data[:300]

        )

        print("\n[+] Readable Preview:")

        print(printable)

    except Exception as e:

        print(
            "[ERROR] Deep scan failed:"
        )

        print(e)

# ============================================
# FILE CARVING
# ============================================

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

                pos = data.find(
                    sig,
                    start
                )

                if pos == -1:

                    break

                positions.append(pos)

                start = pos + 1

            if len(positions) > 1:

                for i, pos in enumerate(
                    positions[1:],
                    start=1
                ):

                    extracted_path = (
                        f"{OUTPUT_DIR}/"
                        f"extracted_{i}.{ext}"
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
                        f"[🚨] Embedded "
                        f"{ext.upper()} extracted:"
                    )

                    print(
                        f"    → {extracted_path}"
                    )

            else:

                print(
                    f"[+] No embedded "
                    f"{ext.upper()} detected"
                )

    except Exception as e:

        print(
            "[ERROR] File carving failed:"
        )

        print(e)

    return extracted_files

# ============================================
# RECURSIVE ANALYSIS
# ============================================

def recursive_scan(extracted_files):

    print("\n[RECURSIVE SCAN]")

    if not extracted_files:

        print(
            "[+] No extracted files "
            "to analyze"
        )

        return

    for path in extracted_files:

        if os.path.isfile(path):

            print(
                f"\n🔁 Re-analyzing: {path}"
            )

            analyze_file(
                path,
                recursive=False
            )

# ============================================
# MAIN ANALYZER
# ============================================

def analyze_file(
    file_path,
    recursive=True
):

    print("\n==============================")

    print(
        f"🔍 ANALYZING FILE: "
        f"{file_path}"
    )

    print("==============================")

    if not os.path.exists(file_path):

        print("[ERROR] File not found")

        return

    print_file_info(file_path)

    # ============================================
    # IMAGE ANALYSIS
    # ============================================

    if file_path.endswith(
        (
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp"
        )
    ):

        extract_from_image(file_path)

    # ============================================
    # DOCUMENT ANALYSIS
    # ============================================

    elif file_path.endswith(
        (
            ".pdf",
            ".docx"
        )
    ):

        extract_from_doc(file_path)

    # ============================================
    # GENERIC ANALYSIS
    # ============================================

    extract_strings(file_path)

    deep_scan(file_path)

    # ============================================
    # FILE CARVING
    # ============================================

    extracted_files = carve_files(
        file_path
    )

    # ============================================
    # RECURSIVE ANALYSIS
    # ============================================

    if recursive:

        recursive_scan(extracted_files)

    print("\n✅ Analysis Completed")

# ============================================
# RUN PROGRAM
# ============================================

if __name__ == "__main__":

    path = input(
        "Enter file path: "
    )

    analyze_file(path)