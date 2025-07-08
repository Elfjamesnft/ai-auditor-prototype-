# 🧠 TrustAudit AI – Prototype

TrustAudit AI is an intelligent audit automation tool that mimics a Chartered Accountant’s mindset. It helps firms and companies quickly identify high-risk transactions, enforce compliance, and generate professional reports with minimal manual work.

---

## 🎯 Key Features

✅ **Risk & Error Detection**
- Configurable thresholds (e.g., flag amounts > $10,000)
- Statistical outlier detection
- Weekend & holiday transaction flags
- Duplicate transaction detection
- Suspicious vendor detection
- Automated risk scoring (0–100)

✅ **Audit Trail & Transparency**
- Full audit logs with timestamps
- Reproducible workflows

✅ **Professional Reporting**
- PDF reports with cover page, summaries, and detailed tables
- Monthly spending trend charts
- Excel exports
- Ready-to-send email delivery

✅ **Configurable Rules**
- Easily modify thresholds and criteria in `config.yaml`

---

## 📂 Project Structure

├── auditor.py # Main analysis engine
├── generate_report.py # PDF & Excel report generator
├── send_email.py # Email automation script
├── config.yaml # All configurable audit rules
├── data/
│ └── sample_transactions.csv # Sample input data
├── reports/
│ ├── audit_report.pdf
│ ├── audit_report.xlsx
│ ├── spending_trend.png
│ ├── flagged_transactions.csv
│ └── audit_trail.log
└── README.md


---

## ⚙️ Quick Start

1️⃣ Install Requirements

```bash
pip install -r requirements.txt
(If needed, also install matplotlib and yagmail)
pip install matplotlib yagmail


2️⃣ Analyze Transactions
python auditor.py

✅ Outputs:

reports/flagged_transactions.csv

reports/audit_trail.log

3️⃣ Generate Reports
python generate_report.py

✅ Outputs:

reports/audit_report.pdf

reports/audit_report.xlsx

reports/spending_trend.png

4️⃣ Email Reports
Edit send_email.py with your credentials:
send_report_email(
    sender_email="your_email@gmail.com",
    app_password="your_app_password",
    recipient_email="client@example.com",
    attachments=["reports/audit_report.pdf", "reports/audit_report.xlsx"]
)
Run:
python send_email.py

📝 Configuration
Edit config.yaml to change rules:
amount_threshold: 10000
outlier_std_dev: 2
flag_weekends: true
suspicious_vendors:
  - VendorX
  - VendorY


💡 Why Use AI Auditor?

Speed: Reduce audit time from weeks to hours

Consistency: No manual error or oversight

Transparency: Clear logs and justifications

Professionalism: Investor- and client-ready reports

🚀 Roadmap

 Web dashboard

 Multi-user authentication

 Interactive review & comments

 More compliance standards

🧑‍💻 Author
Elf James aka Asim Shaikh
Prototype maintained by TrustAudit AI

📄 License
MIT License


