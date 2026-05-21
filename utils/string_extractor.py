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

            print("[+] No readable strings found")

    except Exception as e:

        print("[ERROR] String extraction failed")

        print(e)