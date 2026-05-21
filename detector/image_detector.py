# ============================================
# ADVANCED IMAGE STEGANOGRAPHY DETECTOR
# ============================================

from PIL import Image

import numpy as np

from stegano import lsb

from scipy.stats import chisquare

from utils.entropy_analysis import (
    calculate_entropy
)

# ============================================
# IMAGE ANALYSIS
# ============================================

def analyze_image(image_path):

    print("\n[ADVANCED IMAGE ANALYSIS]")

    score = 0

    hidden_msg = None

    # ============================================
    # LOAD IMAGE
    # ============================================

    try:

        img = Image.open(image_path)

        pixels = np.array(img)

        print("[+] Image loaded successfully")

        print(f"[+] Shape: {pixels.shape}")

    except Exception as e:

        print("[ERROR] Failed to load image")

        print(e)

        return False

    # ============================================
    # LSB EXTRACTION
    # ============================================

    try:

        hidden_msg = lsb.reveal(image_path)

        if hidden_msg:

            print(
                "\n[🚨] Hidden LSB Message Found:"
            )

            # Limit output size
            preview = hidden_msg[:500]

            print(preview)

            if len(hidden_msg) > 500:

                print(
                    "\n[+] Payload truncated..."
                )

            score += 50

        else:

            print(
                "[+] No hidden LSB payload detected"
            )

    except Exception:

        print("[!] LSB extraction failed")

    # ============================================
    # ENTROPY ANALYSIS
    # ============================================

    try:

        entropy = calculate_entropy(
            pixels.flatten()
        )

        print(f"[+] Entropy: {entropy:.4f}")

        # Entropy scoring
        if entropy > 7.0:

            print(
                "[🚨] Extremely high entropy"
            )

            score += 30

        elif entropy > 6.0:

            print(
                "[⚠] Elevated entropy detected"
            )

            score += 20

        elif entropy > 5.2:

            score += 10

    except Exception as e:

        print("[ERROR] Entropy analysis failed")

        print(e)

    # ============================================
    # LSB DISTRIBUTION
    # ============================================

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

        print(
            f"[+] LSB Distribution: {lsb_dict}"
        )

        count_0 = lsb_dict.get(0, 0)

        count_1 = lsb_dict.get(1, 0)

        total = count_0 + count_1

        balance = abs(
            count_0 - count_1
        ) / total

        print(
            f"[+] LSB Balance: {balance:.4f}"
        )

        # ============================================
        # BALANCE SCORING
        # ============================================

        if balance < 0.05:

            print(
                "[🚨] Highly suspicious LSB balancing"
            )

            score += 30

        elif balance < 0.10:

            print(
                "[⚠] Suspicious LSB balancing"
            )

            score += 20

        elif balance < 0.15:

            score += 10

    except Exception as e:

        print("[ERROR] LSB analysis failed")

        print(e)

    # ============================================
    # CHI-SQUARE ANALYSIS
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

        # ============================================
        # CHI SCORE
        # ============================================

        if p_value > 0.9:

            print(
                "[🚨] Strong statistical anomaly"
            )

            score += 20

        elif p_value > 0.7:

            print(
                "[⚠] Moderate statistical anomaly"
            )

            score += 10

    except Exception as e:

        print(
            "[ERROR] Chi-square analysis failed"
        )

        print(e)

    # ============================================
    # FINAL SCORE
    # ============================================

    score = min(score, 100)

    print(
        f"\n[+] Suspicion Score: {score}/100"
    )

    # ============================================
    # FINAL VERDICT
    # ============================================

    if score >= 70:

        print(
            "🚨 HIGHLY SUSPICIOUS IMAGE"
        )

    elif score >= 40:

        print(
            "⚠ POSSIBLY SUSPICIOUS IMAGE"
        )

    else:

        print(
            "✅ LIKELY CLEAN IMAGE"
        )

    # ============================================
    # RETURN RESULTS
    # ============================================

    return {

        "score": score,

        "hidden_message": hidden_msg,

        "entropy": entropy,

        "balance": balance,

        "p_value": p_value

    }