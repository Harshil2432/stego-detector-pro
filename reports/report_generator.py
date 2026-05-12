def generate_report(file_path, status):
    report = f"""
    --------- STEGO ANALYSIS REPORT ---------
    File: {file_path}
    Result: {status}
    ----------------------------------------
    """

    with open("output/report.txt", "a") as f:
        f.write(report)

    print("[+] Report Generated")