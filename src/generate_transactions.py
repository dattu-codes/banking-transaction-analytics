
from datetime import date, timedelta
from pathlib import Path
import random

import pandas as pd

# Reproducible synthetic dataset
rng = random.Random(42)

customers = [f"CUST{i:05d}" for i in range(1, 1001)]

transaction_types = ["DEBIT", "CREDIT"]
channels = ["UPI", "CARD", "NET_BANKING", "ATM", "BANK_TRANSFER"]
statuses = ["SUCCESS", "FAILED", "PENDING", "REVERSED"]
merchant_categories = [
    "GROCERIES",
    "FUEL",
    "SHOPPING",
    "DINING",
    "UTILITIES",
    "TRAVEL",
    "HEALTHCARE",
    "ATM",
    "TRANSFER",
]

records = []

# Generate 5,000 synthetic transactions
for i in range(1, 5001):
    transaction_date = date(2025, 1, 1) + timedelta(
        days=rng.randint(0, 364)
    )

    records.append({
        "transaction_id": f"TXN{i:06d}",
        "customer_id": rng.choice(customers),
        "transaction_date": transaction_date.isoformat(),
        "transaction_type": rng.choice(transaction_types),
        "amount": round(rng.uniform(50, 75000), 2),
        "currency": "INR",
        "channel": rng.choice(channels),
        "status": rng.choice(statuses),
        "merchant_category": rng.choice(merchant_categories),
        "country": "India",
    })

df = pd.DataFrame(records)

# Introduce deliberate data-quality problems.
# 1. Missing customer IDs
for idx in rng.sample(range(len(df)), 40):
    df.at[idx, "customer_id"] = None

# 2. Missing transaction amounts
for idx in rng.sample(range(len(df)), 40):
    df.at[idx, "amount"] = None

# 3. Invalid amounts: negative values and zero amounts
invalid_indices = rng.sample(range(len(df)), 30)

for idx in invalid_indices[:15]:
    df.at[idx, "amount"] = round(-rng.uniform(10, 5000), 2)

for idx in invalid_indices[15:]:
    df.at[idx, "amount"] = 0.00

# 4. Inconsistent status capitalization and whitespace
status_indices = rng.sample(range(len(df)), 75)
status_variants = [
    " success ",
    "SUCCESS ",
    "failed",
    " Failed ",
    " pending",
    "REVERSED ",
]

for idx in status_indices:
    df.at[idx, "status"] = rng.choice(status_variants)

# 5. Add 50 exact duplicate transaction rows
duplicate_rows = df.sample(n=50, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

# Shuffle the rows
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the raw dataset
output_path = Path("data/raw/banking_transactions.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print(f"Output file: {output_path}")
print(f"Total rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Exact duplicate rows: {df.duplicated().sum()}")
print(f"Missing customer IDs: {df['customer_id'].isna().sum()}")
print(f"Missing amounts: {df['amount'].isna().sum()}")
print(f"Non-positive amounts: {(df['amount'].le(0)).sum()}")
