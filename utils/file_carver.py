# ============================================
# FILE CARVING
# ============================================

import os

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================
# CARVING ENGINE
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

        for signature, extension in signatures.items():

            positions = []

            start = 0

            while True:

                pos = data.find(signature, start)

                if pos == -1:

                    break

                positions.append(pos)

                start = pos + 1

            # Ignore original header
            if len(positions) > 1:

                for i, pos in enumerate(
                    positions[1:],
                    start=1
                ):

                    output_path = (

                        f"{OUTPUT_DIR}/"

                        f"extracted_{i}.{extension}"

                    )

                    with open(
                        output_path,
                        "wb"
                    ) as out:

                        out.write(data[pos:])

                    extracted_files.append(
                        output_path
                    )

                    print(

                        f"[🚨] Embedded "

                        f"{extension.upper()} extracted"

                    )

                    print(
                        f"    → {output_path}"
                    )

            else:

                print(

                    f"[+] No embedded "

                    f"{extension.upper()} detected"

                )

    except Exception as e:

        print("[ERROR] File carving failed")

        print(e)

    return extracted_files