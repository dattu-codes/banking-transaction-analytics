

\# Banking Transaction Analytics \& Data Quality Dashboard



An end-to-end data analytics portfolio project using synthetic banking transactions to demonstrate SQL analysis, data cleaning, data quality checks, Excel reporting, and Power BI visualization.



> \*\*Data disclaimer:\*\* All transaction records are synthetic and generated for learning and portfolio purposes. They do not represent real bank customers or actual banking performance.



\## Project Objectives



\- Generate a reproducible transaction dataset with deliberate data-quality issues.

\- Load raw data into PostgreSQL and analyse it with SQL.

\- Deduplicate transactions and standardize inconsistent status values.

\- Identify missing customer IDs and invalid transaction amounts.

\- Build monthly, channel, status, and data-quality summaries.

\- Export results to CSV, Excel, and Power BI.



\## Technology Stack



\- \*\*Python:\*\* Pandas, NumPy, SQLAlchemy, psycopg2, openpyxl

\- \*\*Database:\*\* PostgreSQL

\- \*\*SQL:\*\* Aggregations, CTEs, window functions, conditional counts, views

\- \*\*Reporting:\*\* Microsoft Excel

\- \*\*Visualization:\*\* Power BI Desktop

\- \*\*Version Control:\*\* Git



\## Data Pipeline



1\. Generate 5,000 synthetic transactions.

2\. Add 50 duplicate records and deliberate data-quality issues.

3\. Load 5,050 rows into the PostgreSQL raw staging table.

4\. Create a cleaned table with 5,000 rows by retaining one record per transaction ID.

5\. Standardize statuses and flag missing customer IDs and invalid amounts.

6\. Create SQL views for monthly trends, channel performance, status distribution, and data quality.

7\. Export analytics to CSV and create an Excel workbook.

8\. Visualize the results in Power BI.



\## Key Data Quality Checks



\- Duplicate transaction records

\- Missing customer IDs

\- Missing transaction amounts

\- Zero or negative transaction amounts

\- Inconsistent status capitalization and whitespace

\- Reconciliation between raw and cleaned row counts



Invalid or missing amounts are represented as NULL in the cleaned output and identified using quality flags. Missing customer IDs are flagged rather than filled with invented values.



\## Project Structure



```text

banking-transaction-analytics/

├── data/

│   ├── raw/

│   └── cleaned/

├── src/

│   ├── generate\_transactions.py

│   ├── load\_raw\_to\_postgres.py

│   ├── export\_analytics.py

│   └── create\_excel\_workbook.py

├── sql/

│   ├── 01\_schema.sql

│   └── 02\_cleaning\_and\_views.sql

├── excel/

│   └── Banking\_Transaction\_Analytics.xlsx

├── powerbi/

│   └── Banking\_Transaction\_Analytics.pbix

├── reports/

├── requirements.txt

├── .gitignore

└── README.md

```



\## How to Run



\### 1. Install Python dependencies



```powershell

python -m venv venv

.\\venv\\Scripts\\python.exe -m pip install -r requirements.txt

```



\### 2. Generate the synthetic dataset



```powershell

.\\venv\\Scripts\\python.exe src/generate\_transactions.py

```



\### 3. Set up PostgreSQL



Create a database named `banking\_analytics` and execute `sql/01\_schema.sql` using pgAdmin's Query Tool.



\### 4. Load the raw data



```powershell

.\\venv\\Scripts\\python.exe src/load\_raw\_to\_postgres.py

```



Enter your PostgreSQL password when prompted.



\### 5. Clean and analyse the data



Execute `sql/02\_cleaning\_and\_views.sql` in the `banking\_analytics` database after loading the raw data.



\### 6. Export the analysis



```powershell

.\\venv\\Scripts\\python.exe src/export\_analytics.py

```



\### 7. Create the Excel workbook



```powershell

.\\venv\\Scripts\\python.exe src/create\_excel\_workbook.py

```



Open the Power BI report in Power BI Desktop to explore the monthly trends, transaction channels, status distribution, and data-quality checks.



\## Important Notes



\- The dataset is synthetic, and transaction statuses are randomly assigned.

\- Success rates and transaction values are illustrative, not real-world banking benchmarks.

\- Quality flags preserve visibility into records requiring investigation.



