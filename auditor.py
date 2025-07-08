import pandas as pd
import numpy as np
import yaml
import datetime

# Load configurable thresholds from a YAML file
def load_config(config_file="config.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

def analyze_transactions(csv_file, config_file="config.yaml"):
    df = pd.read_csv(csv_file)
    config = load_config(config_file)

    flagged = []

    # For audit trail
    audit_log = []

    # Calculate outlier threshold
    mean_amount = df["Amount"].mean()
    std_amount = df["Amount"].std()
    outlier_threshold = mean_amount + (config["outlier_std_dev"] * std_amount)

    # Duplicate detection
    duplicates = df[df.duplicated(subset=["Date", "Description", "Amount"], keep=False)]
    duplicate_indices = set(duplicates.index)

    for idx, row in df.iterrows():
        reasons = []
        if row["Amount"] > config["amount_threshold"]:
            reasons.append(f"Amount > {config['amount_threshold']}")
        if row["Amount"] > outlier_threshold:
            reasons.append("Statistical outlier")
        if idx in duplicate_indices:
            reasons.append("Duplicate transaction")

        if reasons:
            flagged.append({
                "Date": row["Date"],
                "Description": row["Description"],
                "Amount": row["Amount"],
                "Notes": "; ".join(reasons)
            })
            audit_log.append(f"{row['Date']} {row['Description']} flagged: {', '.join(reasons)}")

    # Save audit trail
    with open("reports/audit_trail.log", "w") as log_file:
        for line in audit_log:
            log_file.write(line + "\n")

    flagged_df = pd.DataFrame(flagged)
    flagged_df.to_csv("reports/flagged_transactions.csv", index=False)
    print("Analysis complete. Flagged transactions saved to CSV and audit trail log generated.")

    return flagged_df
