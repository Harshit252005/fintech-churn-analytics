import duckdb
import pandas as pd

# Connect DuckDB
con = duckdb.connect()

# Load CSVs directly into in-memory SQL tables
con.execute("CREATE TABLE users AS SELECT * FROM 'data/users.csv'")
con.execute("CREATE TABLE transactions AS SELECT * FROM 'data/transactions.csv'")

print("Executing SQL Queries via DuckDB...")

# 1. Run RFM
with open("sql/rfm_segmentation.sql", "r") as f:
    rfm_sql = f.read()
rfm_df = con.execute(rfm_sql).fetchdf()
print("\n--- RFM Segmentation Head ---")
print(rfm_df.head())

# 2. Run Cohort Matrix
with open("sql/cohort_analysis.sql", "r") as f:
    cohort_sql = f.read()
cohort_df = con.execute(cohort_sql).fetchdf()
print("\n--- Cohorts Head ---")
print(cohort_df.head())

# 3. Run Category CLV
with open("sql/category_clv.sql", "r") as f:
    clv_sql = f.read()
clv_df = con.execute(clv_sql).fetchdf()
print("\n--- Category CLV & AOV ---")
print(clv_df)