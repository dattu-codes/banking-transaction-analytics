# Banking Transaction Analytics & Data Quality Dashboard

**An end-to-end data analytics project using Python, PostgreSQL, SQL, Microsoft Excel, and Power BI.**

Transforming raw transaction data into structured, quality-checked datasets and business-focused analytics.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge&logo=databricks&logoColor=white)
![Microsoft Excel](https://img.shields.io/badge/Excel-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)

> **Data disclaimer:** This project uses entirely synthetic transaction data generated for educational and portfolio purposes. It contains no real customer records. Transaction outcomes are randomly generated, so the results must not be interpreted as actual banking performance.

---

## Overview

Financial transaction data is useful only when it is accurate, consistent, and ready for analysis. Missing customer identifiers, duplicate records, invalid amounts, and inconsistent status values can undermine reporting and operational decisions.

This project demonstrates an end-to-end analytics workflow that starts with raw synthetic transaction records and produces cleaned data, SQL-based analytical views, Excel reports, and a Power BI dashboard.

The focus is on practical data analyst skills: **data preparation, SQL querying, data-quality validation, aggregation, reconciliation, reporting, and visualization.**

## Project Highlights

| Metric | Result |
|---|---:|
| Raw transaction rows | 5,050 |
| Cleaned transaction rows | 5,000 |
| Duplicate rows removed | 50 |
| Missing customer IDs in cleaned data | 40 |
| Missing transaction amounts in cleaned data | 40 |
| Zero or negative amounts in cleaned data | 30 |
| Nonstandard statuses after cleaning | 0 |

These figures are results from the generated dataset and the completed cleaning workflow, not real-world banking statistics.

## Business Questions

The analysis is designed to answer questions such as:

- How does transaction volume change month by month?
- How do transaction volumes and success rates differ across channels?
- What is the distribution of successful, failed, pending, and reversed transactions?
- How much recorded value is associated with successful transactions?
- How many records contain missing identifiers or invalid amounts?
- How do raw and cleaned record counts reconcile after deduplication?

## Data Quality and Preparation

The dataset contains 5,000 generated transactions, with 50 additional duplicate rows and deliberately introduced data-quality issues.

The workflow addresses the following problems:

- **Duplicate records:** Identifies repeated transaction IDs and retains one record per transaction ID.
- **Inconsistent statuses:** Removes surrounding whitespace and standardizes capitalization, such as converting ` success ` and `failed` to their canonical forms.
- **Missing customer IDs:** Flags incomplete identifiers for investigation rather than inventing customer values.
- **Missing amounts:** Preserves missing amounts as SQL `NULL` in the cleaned table.
- **Invalid amounts:** Converts zero and negative amounts to `NULL` in the cleaned table while preserving an `amount_quality` flag.
- **Reconciliation:** Compares raw and cleaned record counts to quantify the effect of deduplication.

Two quality flags are added to the cleaned data:

- `amount_quality`: `VALID`, `MISSING`, or `NON_POSITIVE`
- `customer_id_quality`: `VALID` or `MISSING`

This approach preserves records that require investigation rather than silently deleting every record with a quality issue.

## Analytics and Dashboard

### 1. Transaction Trends

Monthly SQL summaries provide transaction volumes, successful transaction counts, success rates, recorded successful transaction amounts, and data-quality issue counts.

### 2. Channel Performance

Channel-level summaries compare transaction volumes, outcomes, success rates, successful transaction values, and amount-quality issues.

### 3. Transaction Status Distribution

The analysis groups transactions into four standardized statuses:

- `SUCCESS`
- `FAILED`
- `PENDING`
- `REVERSED`

### 4. Data Quality Scorecard

The reconciliation summary reports raw and cleaned record counts, duplicate rows removed, missing customer IDs, missing amounts, non-positive amounts, and any nonstandard statuses remaining after cleaning.

### 5. Excel Reporting and Power BI

The project includes an Excel workbook with summary worksheets, KPI formulas, and charts, plus a Power BI report for visual exploration of transaction trends and data-quality measures.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Dataset generation, database loading, exports, and workbook creation |
| Pandas | Data manipulation and CSV processing |
| NumPy | Numerical data processing dependency |
| PostgreSQL | Raw staging tables and cleaned analytical data |
| SQL | CTEs, window functions, aggregations, conditional counts, and views |
| SQLAlchemy and psycopg2 | Python-to-PostgreSQL connectivity |
| Microsoft Excel | Reporting workbook, formulas, tables, and charts |
| Power BI Desktop | Interactive report development |
| Git and GitHub | Version control and project hosting |

## Project Architecture

```text
Synthetic Transaction Generator
              |
              v
     Raw CSV Dataset
       5,050 rows
              |
              v
      PostgreSQL Staging
       raw_transactions
              |
              v
      SQL Cleaning Layer
   Deduplication and Standardization
              |
              v
     cleaned_transactions
        5,000 rows
              |
              v
       Analytical SQL Views
    /          |           \
   v           v            v
Monthly      Channel      Status and
Summary      Summary      Quality Views
    \          |           /
              v
       Python CSV Exports
              |
        +-----+------+
        |            |
        v            v
   Excel Workbook  Power BI Report
```

## Repository Structure

```text
banking-transaction-analytics/
├── data/
│   ├── raw/
│   │   └── banking_transactions.csv
│   └── cleaned/
│       ├── cleaned_transactions.csv
│       ├── monthly_summary.csv
│       ├── channel_summary.csv
│       ├── status_summary.csv
│       └── data_quality_summary.csv
├── src/
│   ├── generate_transactions.py
│   ├── load_raw_to_postgres.py
│   ├── export_analytics.py
│   └── create_excel_workbook.py
├── sql/
│   ├── 01_schema.sql
│   └── 02_cleaning_and_views.sql
├── excel/
│   └── Banking_Transaction_Analytics.xlsx
├── powerbi/
│   └── Banking_Transaction_Analytics.pbix
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version
- PostgreSQL 18 or a compatible PostgreSQL version
- pgAdmin 4 or another PostgreSQL client
- Microsoft Excel or a compatible spreadsheet application
- Power BI Desktop to open and explore the `.pbix` report

### 1. Clone the repository

```powershell
git clone https://github.com/dattu-codes/banking-transaction-analytics.git
cd banking-transaction-analytics
```

### 2. Create the Python environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. Generate the synthetic dataset

```powershell
.\venv\Scripts\python.exe src/generate_transactions.py
```

This generates the raw CSV at `data/raw/banking_transactions.csv`.

### 4. Create the PostgreSQL database

In pgAdmin, create a database named `banking_analytics`.

Open its Query Tool and execute:

```text
sql/01_schema.sql
```

This creates the `raw_transactions` staging table.

### 5. Load the raw data

Run:

```powershell
.\venv\Scripts\python.exe src/load_raw_to_postgres.py
```

Enter the PostgreSQL password when prompted. The script loads the CSV into the raw staging table and reports the number of records inserted.

### 6. Clean and analyse the data

In pgAdmin, open the Query Tool connected to `banking_analytics` and execute:

```text
sql/02_cleaning_and_views.sql
```

This creates the cleaned table and analytical views. **Note:** This script drops and recreates `cleaned_transactions`, so execute it only when you intend to rebuild the cleaned output.

### 7. Export the analytical results

```powershell
.\venv\Scripts\python.exe src/export_analytics.py
```

The CSV summaries are saved under `data/cleaned/`.

### 8. Create the Excel workbook

```powershell
.\venv\Scripts\python.exe src/create_excel_workbook.py
```

The workbook is written to:

```text
excel/Banking_Transaction_Analytics.xlsx
```

### 9. Open the Power BI report

Open:

```text
powerbi/Banking_Transaction_Analytics.pbix
```

If Power BI requests the Excel source file on another computer, update the source path to the workbook included in this repository.

## Data and Interpretation Notes

- The transaction dataset covers dates in 2025.
- Transaction IDs are generated identifiers, not actual bank reference numbers.
- Transaction statuses are randomly assigned and do not model real payment-processing behaviour.
- Success rates, transaction values, and channel comparisons are illustrative only.
- Missing or invalid amounts are flagged and treated as `NULL` in the cleaned dataset; they are not replaced with fabricated values.
- The project demonstrates a portfolio workflow and is not intended for production banking use.

## Possible Future Enhancements

- Add automated Python unit tests for data-quality rules.
- Build a more comprehensive reconciliation report with explicit validation assertions.
- Add date and channel filters, drill-through pages, and improved data-quality tooltips in Power BI.
- Add a repeatable orchestration workflow for dataset generation, database loading, cleaning, and export.
- Add automated tests to verify transaction-count and quality-metric invariants after each run.

## Author

**Dattatreya Teella**

GitHub: [@dattu-codes](https://github.com/dattu-codes)

Project repository: [banking-transaction-analytics](https://github.com/dattu-codes/banking-transaction-analytics)

---

*Built as a practical data analytics portfolio project to demonstrate Python, PostgreSQL, SQL, Excel, and Power BI skills.*
