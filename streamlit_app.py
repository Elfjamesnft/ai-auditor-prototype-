import streamlit as st
import pandas as pd
import os
from auditor import analyze_transactions
from generate_report import generate_audit_report

st.set_page_config(page_title="TrustAudit AI", layout="wide")

st.title("🔍 TrustAudit AI")
st.subheader("AI-Powered Clarity for Every Transaction")

uploaded_file = st.file_uploader("Upload a CSV file with transactions", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of your data:")
    st.dataframe(df.head())

    if st.button("Run Audit"):
        # Save uploaded file to a temporary location
        input_path = "data/temp_transactions.csv"
        df.to_csv(input_path, index=False)

        st.info("Analyzing transactions...")
        flagged_items = analyze_transactions(input_path)

        st.success(f"Audit completed. {len(flagged_items)} flagged transactions found.")
        st.write(flagged_items)

        # Save flagged transactions
        flagged_csv = "reports/flagged_transactions.csv"
        flagged_items.to_csv(flagged_csv, index=False)

        # Generate reports
        pdf_report, excel_report, chart_path = generate_audit_report(input_path)

        st.subheader("📄 Reports & Exports")

        with open(pdf_report, "rb") as f:
            st.download_button(
                label="Download PDF Report",
                data=f,
                file_name="audit_report.pdf",
                mime="application/pdf",
            )

        with open(excel_report, "rb") as f:
            st.download_button(
                label="Download Excel Report",
                data=f,
                file_name="audit_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

        st.image(chart_path, caption="Spending Trend")

        st.success("All done!")

