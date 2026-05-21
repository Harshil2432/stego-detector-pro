# 🔐 STEGO-ANALYZER
### Advanced Digital Forensics & Steganography Detection Suite

A professional cybersecurity and digital forensics framework designed for detecting steganography, hidden payloads, embedded files, suspicious metadata, and forensic anomalies across images, documents, and multimedia files.

---

# 🚀 Key Features

## 🔍 Advanced Steganography Detection
- Least Significant Bit (LSB) Analysis
- Hidden Payload Extraction
- Statistical Steganalysis
- Chi-Square Distribution Testing
- Entropy-Based Detection
- Online Stego Tool Detection

## 📂 Universal Forensic Scanning
- Recursive Folder Scanning
- Embedded File Extraction
- Deep Binary Analysis
- HEX Inspection
- Readable String Extraction
- Suspicious Keyword Detection

## 🖼️ Image Forensics
- PNG/JPG/BMP Analysis
- Entropy Visualization
- Metadata & EXIF Inspection
- LSB Bit Distribution Analysis
- Hidden Message Recovery
- Suspicion Scoring Engine

## 📄 Document Forensics
- PDF Analysis
- DOCX Inspection
- Metadata Extraction
- Embedded Artifact Detection

## 📊 Reporting & Visualization
- Automated PDF Report Generation
- Risk Classification Engine
- Timestamped Logs
- Real-Time GUI Monitoring
- Dark-Themed DFIR Dashboard

---

# 🧠 Detection Techniques

| Technique | Purpose |
|---|---|
| LSB Analysis | Detect hidden pixel manipulation |
| Entropy Analysis | Detect randomness anomalies |
| Chi-Square Testing | Statistical steganalysis |
| File Carving | Recover embedded payloads |
| Metadata Inspection | Detect suspicious EXIF tags |
| Deep Binary Scan | Detect hidden keywords/artifacts |
| Recursive Analysis | Analyze extracted embedded files |

---

# 🛠️ Technologies Used

| Technology | Usage |
|---|---|
| Python | Core Framework |
| Tkinter | GUI Interface |
| NumPy | Matrix & Pixel Operations |
| SciPy | Statistical Analysis |
| Pillow (PIL) | Image Processing |
| Stegano | LSB Extraction |
| ReportLab | PDF Reporting |
| PyPDF2 | PDF Analysis |
| python-docx | DOCX Inspection |
| OpenCV | Image Processing |
| exifread | Metadata Analysis |

---

# 📂 Project Structure

```text
stego-analyzer/
│
├── forensic_gui.py
├── universal_extractor.py
├── pdf_report.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── detector/
│   ├── image_detector.py
│   ├── document_detector.py
│   ├── audio_detector.py
│   └── video_detector.py
│
├── utils/
│   ├── entropy_analysis.py
│   ├── file_carver.py
│   ├── deep_scan.py
│   └── string_extractor.py
│
├── alert/
├── samples/
├── screenshots/
├── output/
└── reports/
```

---

# ⚡ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/stego-analyzer.git
```

---

## 2️⃣ Open Project

```bash
cd stego-analyzer
```

---

## 3️⃣ Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

## GUI Mode

```bash
python forensic_gui.py
```

---

## Terminal Mode

```bash
python universal_extractor.py
```

---

# 📸 Screenshots

Add screenshots inside:

```text
screenshots/
```

Recommended screenshots:
- gui_dashboard.png
- clean_image_scan.png
- suspicious_image_scan.png
- pdf_report.png

---

# 🧪 Sample Testing

Store forensic samples inside:

```text
samples/
```

Recommended:
- clean_image.png
- stego_image.png
- futureboy_stego.jpg
- suspicious_payload.png

---

# 🔬 Real-World Testing

This framework supports testing against:
- Custom LSB payloads
- Online Steganography Encoders
- Stegano-generated images
- Suspicious embedded payloads
- Recursive extracted artifacts

---

# 🎓 Academic & Research Usage

This project was developed for:
- Digital Forensics
- Cybersecurity Research
- DFIR Training
- Malware Investigation
- Steganography Detection
- CTF Analysis
- Incident Response Learning

---

# ⚠ Disclaimer

This tool is intended strictly for:
- educational purposes
- cybersecurity research
- ethical forensic analysis
- academic learning

The author is not responsible for misuse of this software.

---

# 👨‍💻 Author

## Harshil S Parekh

Cybersecurity & Digital Forensics Researcher

Specialized in:
- Digital Forensics
- Steganography Detection
- Malware Analysis
- DFIR Research
- Cybersecurity Tool Development

---

# 📜 License

This project is licensed under the MIT License.