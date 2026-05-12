from PIL import Image
import numpy as np
from stegano import lsb
from utils.entropy_analysis import calculate_entropy

def detect_lsb(image_path):
    try:
        img = Image.open(image_path)
        pixels = np.array(img)

        # LSB Analysis
        lsb_bits = pixels & 1
        unique, counts = np.unique(lsb_bits, return_counts=True)

        lsb_dict = {int(k): int(v) for k, v in zip(unique, counts)}
        print("[+] LSB Distribution:", lsb_dict)

        count_0 = lsb_dict.get(0, 0)
        count_1 = lsb_dict.get(1, 0)

        total = count_0 + count_1
        ratio = count_1 / total if total > 0 else 0

        print(f"[+] LSB 1-bit ratio: {ratio:.6f}")

        # Entropy
        entropy = calculate_entropy(pixels.flatten())
        print(f"[+] Entropy: {entropy:.4f}")

        # Confidence
        confidence = int((ratio * 100) + (entropy * 5))
        confidence = min(confidence, 100)
        print(f"[+] Confidence Score: {confidence}%")

        # Balance
        balance = abs(count_0 - count_1) / total if total > 0 else 0
        print(f"[+] LSB Balance: {balance:.4f}")

        # Detection logic
        suspicious = False
        if (ratio > 0.3 and entropy > 6.5) or balance < 0.02:
            print("[!] Suspicious (statistical detection)")
            suspicious = True
        else:
            print("[+] Likely clean (statistical)")

        # 🔓 ALWAYS attempt extraction
        try:
            hidden_msg = lsb.reveal(image_path)
            if hidden_msg:
                print("[+] Hidden Message Found:", hidden_msg)
                suspicious = True
            else:
                print("[+] No hidden message detected via extraction")
        except Exception as e:
            print("[ERROR extracting message]", e)

        # FINAL DECISION
        if suspicious:
            return True, "Suspicious Image (Detected or Extracted)"
        else:
            return False, "Clean Image"

    except Exception as e:
        print("[ERROR]", e)
        return False, "Error processing image"