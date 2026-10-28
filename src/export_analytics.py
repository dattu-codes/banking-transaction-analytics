
from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

project_dir = Path(__file__).resolve().parent.parent
output_dir = project_dir / "data" / "cleaned"
output_dir.mkdir(parents=True, exist_ok=True)

password = getpass("PostgreSQL password: ")

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=password,
    host="localhost",
    port=5432,
    database="banking_analytics",
)

engine = create_engine(connection_url)

exports = {
    "cleaned_transactions.csv":
        "SELECT * FROM cleaned_transactions ORDER BY transaction_date, transaction_id",
    "monthly_summary.csv":
        "SELECT * FROM vw_monthly_transaction_summary ORDER BY transaction_month",
    "channel_summary.csv":
        "SELECT * FROM vw_channel_summary ORDER BY total_transactions DESC",
    "status_summary.csv":
        "SELECT * FROM vw_status_summary ORDER BY status",
    "data_quality_summary.csv":
        "SELECT * FROM vw_data_quality_summary",
}

try:
    with engine.connect() as connection:
        for filename, query in exports.items():
            df = pd.read_sql_query(query, connection)
            output_path = output_dir / filename
            df.to_csv(output_path, index=False)
            print(f"Exported {filename}: {len(df)} rows")

    print(f"\nAll exports saved to: {output_dir}")

finally:
    engine.dispose()
