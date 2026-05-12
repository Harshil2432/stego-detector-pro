import datetime

def generate_alert(file_path, result):
    timestamp = datetime.datetime.now()

    alert_msg = f"""
==============================
🚨 STEGANOGRAPHY ALERT 🚨
File: {file_path}
Time: {timestamp}
Result: {result}
==============================
"""

    print(alert_msg)

    with open("output/alerts.log", "a") as f:
        f.write(alert_msg + "\n")