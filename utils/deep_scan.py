# ============================================
# DEEP FILE SCAN
# ============================================

def deep_scan(file_path):

    print("\n[DEEP SCAN]")

    try:

        with open(file_path, "rb") as f:

            data = f.read()

        # ============================================
        # HEX PREVIEW
        # ============================================

        print("[+] HEX Preview:")

        print(data[:64].hex())

        # ============================================
        # READABLE PREVIEW
        # ============================================

        printable = ''.join(

            chr(b)

            if 32 <= b <= 126

            else '.'

            for b in data[:300]

        )

        print("\n[+] Readable Preview:")

        print(printable)

        # ============================================
        # KEYWORD DETECTION
        # ============================================

        keywords = [

            b"password",
            b"secret",
            b"hidden",
            b"token",
            b"apikey",
            b"flag",
            b"ctf"

        ]

        for keyword in keywords:

            if keyword in data.lower():

                print(

                    f"[🚨] Keyword detected: "

                    f"{keyword.decode()}"

                )

    except Exception as e:

        print("[ERROR] Deep scan failed")

        print(e)