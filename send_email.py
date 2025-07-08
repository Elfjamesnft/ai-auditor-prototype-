import yagmail

def send_report_email(
    sender_email,
    app_password,
    recipient_email,
    subject="AI Audit Report",
    body="Please find attached the latest audit report.",
    attachments=None
):
    yag = yagmail.SMTP(sender_email, app_password)
    yag.send(
        to=recipient_email,
        subject=subject,
        contents=body,
        attachments=attachments
    )
    print("✅ Email sent successfully.")

if __name__ == "__main__":
    send_report_email(
        sender_email="your_email@gmail.com",
        app_password="your_app_password",
        recipient_email="client@example.com",
        attachments=["reports/audit_report.pdf", "reports/audit_report.xlsx"]
    )
