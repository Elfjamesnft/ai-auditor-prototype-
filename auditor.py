import pandas as pd
import numpy as np
import yaml
import datetime

def load_config(config_file="config.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

def analyze_transactions(csv_file, config_file="config.yaml"):
    df = pd.read_csv(csv_file)
    config = load_config(config_file)

    flagged = []
    audit_log = []

    # Calculate statistical outlier threshold
    mean_amount = df["Amount"].mean()
    std_amount = df["Amount"].std()
    outlier_threshold = mean_amount + (config["outlier_std_dev"] * std_amount)

    # Detect duplicates
    duplicates = df[df.duplicated(subset=["Date", "Description", "Amount"], keep=False)]
    duplicate_indices = set(duplicates.index)

    for idx, row in df.iterrows():
        reasons = []
        score = 0

        # Amount threshold
        if row["Amount"] > config["amount_threshold"]:
            reasons.append(f"Amount > {config['amount_threshold']}")
            score += 40

        # Outlier
        if row["Amount"] > outlier_threshold:
            reasons.append("Statistical outlier")
            score += 30

        # Weekend flag
        if config["flag_weekends"]:
            date_obj = pd.to_datetime(row["Date"])
            if date_obj.weekday() >= 5:
                reasons.append("Weekend transaction")
                score += 10

        # Suspicious vendors
        if row["Description"] in config["suspicious_vendors"]:
            reasons.append("Vendor in suspicious list")
            score += 20

        # Duplicate transaction
        if idx in duplicate_indices:
            reasons.append("Duplicate transaction")
            score += 20

        # If any reason found
        if reasons:
            flagged.append({
                "Date": row["Date"],
                "Description": row["Description"],
                "Amount": row["Amount"],
                "Notes": "; ".join(reasons),
                "RiskScore": min(score, 100)
            })
            audit_log.append(f"{row['Date']} {row['Description']} flagged: {', '.join(reasons)} (RiskScore: {min(score,100)})")

    # Save flagged transactions
    flagged_df = pd.DataFrame(flagged)
    flagged_df.to_csv("reports/flagged_transactions.csv", index=False)

    # Save audit trail log
    with open("reports/audit_trail.log", "w") as log_file:
        for line in audit_log:
            log_file.write(line + "\n")

    print("✅ Analysis complete. CSV and audit trail generated.")
    return flagged_df

if __name__ == "__main__":
    analyze_transactions("data/sample_transactions.csv")
