from fpdf import FPDF

def create_report(flagged_items, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Audit Report", ln=True)

    pdf.set_font("Arial", "", 12)
    for item in flagged_items:
        pdf.cell(0, 10, f"Date: {item['Date']}", ln=True)
        pdf.cell(0, 10, f"Description: {item['Description']}", ln=True)
        pdf.cell(0, 10, f"Amount: {item['Amount']}", ln=True)
        pdf.cell(0, 10, f"Reason: {item['Reason']}", ln=True)
        pdf.ln(5)

    pdf.output(output_file)
    print(f"Report saved as {output_file}")

if __name__ == "__main__":
    from auditor import analyze_transactions
    flagged = analyze_transactions("data/sample_transactions.csv")
    create_report(flagged, "reports/audit_report.pdf")
