import pandas as pd

def analyze_transactions(csv_file):
    df = pd.read_csv(csv_file)
    flagged = []

    for index, row in df.iterrows():
        if abs(row["Amount"]) > 1000:
            flagged.append({
                "Date": row["Date"],
                "Description": row["Description"],
                "Amount": row["Amount"],
                "Reason": "High-value transaction"
            })
        if "suspicious" in row["Description"].lower():
            flagged.append({
                "Date": row["Date"],
                "Description": row["Description"],
                "Amount": row["Amount"],
                "Reason": "Suspicious description"
            })

    return flagged

if __name__ == "__main__":
    flagged_items = analyze_transactions("data/sample_transactions.csv")
    for item in flagged_items:
        print(item)
