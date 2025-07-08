from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import datetime
import matplotlib.pyplot as plt

def generate_trend_chart(datafile="data/sample_transactions.csv", output_image="reports/spending_trend.png"):
    df = pd.read_csv(datafile)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M")

    monthly_totals = df.groupby("Month")["Amount"].sum()
    plt.figure(figsize=(8,4))
    monthly_totals.plot(kind="line", marker="o")
    plt.title("Monthly Spend Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spend ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_image)
    plt.close()
    print("✅ Trend chart generated.")

def generate_audit_report(datafile="reports/flagged_transactions.csv", trend_image="reports/spending_trend.png", outputfile="reports/audit_report.pdf"):
    df = pd.read_csv(datafile)

    doc = SimpleDocTemplate(outputfile, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Cover Page
    title = Paragraph("<b>AI Auditor – Automated Audit Report</b>", styles["Title"])
    client = Paragraph("Client: XYZ Company", styles["Normal"])
    date = Paragraph(f"Date: {datetime.date.today().strftime('%d %B %Y')}", styles["Normal"])
    elements.extend([title, Spacer(1,20), client, date, Spacer(1,20), PageBreak()])

    # Summary
    summary_title = Paragraph("<b>Summary of Findings</b>", styles["Heading2"])
    summary_text = f"""
    <br/>
    - Total flagged transactions: {len(df)}<br/>
    - Risk Scores range: {df['RiskScore'].min()}–{df['RiskScore'].max()}<br/>
    """
    elements.extend([summary_title, Spacer(1,12), Paragraph(summary_text, styles["Normal"]), PageBreak()])

    # Trend Chart
    trend_title = Paragraph("<b>Monthly Spending Trend</b>", styles["Heading2"])
    elements.append(trend_title)
    elements.append(Spacer(1,12))
    elements.append(Image(trend_image, width=500, height=250))
    elements.append(PageBreak())

    # Detailed Table
    detail_title = Paragraph("<b>Flagged Transactions</b>", styles["Heading2"])
    elements.append(detail_title)
    elements.append(Spacer(1,12))

    table_data = [["Date", "Description", "Amount ($)", "Notes", "Risk Score"]]
    for _, row in df.iterrows():
        table_data.append([
            row["Date"],
            row["Description"],
            f"{row['Amount']:,.2f}",
            row["Notes"],
            str(row["RiskScore"])
        ])

    table = Table(table_data, colWidths=[70,150,70,150,50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e2a38")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN',(2,1),(-1,-1),'RIGHT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey])
    ]))

    elements.append(table)

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    print("✅ PDF report with trend chart generated.")

def add_footer(canvas_obj, doc):
    page_num = canvas_obj.getPageNumber()
    text = f"AI Auditor – Confidential | Page {page_num}"
    canvas_obj.setFont("Helvetica", 9)
    canvas_obj.setFillColor(colors.grey)
    canvas_obj.drawString(40, 20, text)

def export_excel_report(datafile="reports/flagged_transactions.csv", outputfile="reports/audit_report.xlsx"):
    df = pd.read_csv(datafile)
    with pd.ExcelWriter(outputfile) as writer:
        df.to_excel(writer, index=False, sheet_name="Flagged Transactions")
    print("✅ Excel report generated.")

if __name__ == "__main__":
    generate_trend_chart()
    generate_audit_report()
    export_excel_report()
