
from getpass import getpass
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Locate the CSV relative to the project directory
project_dir = Path(__file__).resolve().parent.parent
csv_path = project_dir / "data" / "raw" / "banking_transactions.csv"

df = pd.read_csv(csv_path)

# Convert dates to Python date objects for PostgreSQL
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"], errors="raise"
).dt.date

# Convert pandas missing values (NaN/NaT) to SQL NULL
df = df.astype(object).where(pd.notna(df), None)
rows = list(df.itertuples(index=False, name=None))

password = getpass("Enter PostgreSQL password for user postgres: ")

conn = None

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="banking_analytics",
        user="postgres",
        password=password,
    )

    with conn.cursor() as cur:
        # Make reruns safe by replacing existing raw-table contents
        cur.execute("TRUNCATE TABLE raw_transactions")

        insert_sql = """
            INSERT INTO raw_transactions (
                transaction_id,
                customer_id,
                transaction_date,
                transaction_type,
                amount,
                currency,
                channel,
                status,
                merchant_category,
                country
            ) VALUES %s
        """

        execute_values(cur, insert_sql, rows, page_size=1000)

        cur.execute("SELECT COUNT(*) FROM raw_transactions")
        total_rows = cur.fetchone()[0]

    conn.commit()
    print("Data loaded successfully!")
    print(f"CSV records: {len(df)}")
    print(f"Database records: {total_rows}")

except Exception:
    if conn is not None:
        conn.rollback()
    raise

finally:
    if conn is not None:
        conn.close()
