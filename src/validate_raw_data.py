
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw" / "banking_transactions.csv"

df = pd.read_csv(CSV_PATH)

# Convert transaction amounts to numeric values.
amount = pd.to_numeric(df["amount"], errors="coerce")

# Use NumPy to classify amount-quality issues.
df["amount_quality_audit"] = np.select(
    [
        amount.isna(),
        amount.le(0),
    ],
    [
        "MISSING",
        "NON_POSITIVE",
    ],
    default="VALID",
)

# Use NumPy to flag missing or blank customer IDs.
customer_ids = df["customer_id"].astype("string").str.strip()

df["customer_id_quality_audit"] = np.where(
    customer_ids.isna() | customer_ids.eq(""),
    "MISSING",
    "VALID",
)

# Standardize transaction statuses for validation.
standard_statuses = {"SUCCESS", "FAILED", "PENDING", "REVERSED"}
normalized_statuses = df["status"].astype("string").str.strip().str.upper()

# Print the audit report.
print("BANKING TRANSACTION DATA QUALITY AUDIT")
print("-" * 42)
print(f"Total raw rows: {len(df)}")
print(f"Exact duplicate rows: {df.duplicated().sum()}")
print(
    "Extra duplicate transaction IDs: "
    f"{df['transaction_id'].duplicated().sum()}"
)
print(
    "Missing customer IDs: "
    f"{(df['customer_id'].isna() | customer_ids.eq('')).sum()}"
)
print(
    "Missing amounts: "
    f"{(df['amount_quality_audit'] == 'MISSING').sum()}"
)
print(
    "Zero or negative amounts: "
    f"{(df['amount_quality_audit'] == 'NON_POSITIVE').sum()}"
)
print(
    "Statuses requiring standardization: "
    f"{(~normalized_statuses.isin(standard_statuses)).sum()}"
)

print("\nAmount quality breakdown:")
print(df["amount_quality_audit"].value_counts().to_string())

print("\nAudit completed successfully.")
