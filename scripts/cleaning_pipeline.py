# """
# FINAL STABLE CLEANING PIPELINE
# Customer Revenue & Support Analysis

# Fixes:
# - Power BI relationship errors (duplicate customer_id)
# - safe datatypes for joins
# - minimal safe cleaning (no KPI break)
# """

# import os
# import pandas as pd
# import numpy as np
# import logging

# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# RAW_PATH = "data/raw"
# CLEAN_PATH = "data/clean"

# os.makedirs(CLEAN_PATH, exist_ok=True)

# # -------------------------------------------------
# # LOAD DATA
# # -------------------------------------------------

# logging.info("Loading raw data...")

# customers = pd.read_csv(f"{RAW_PATH}/customers.csv")
# transactions = pd.read_csv(f"{RAW_PATH}/transactions.csv")
# tickets = pd.read_csv(f"{RAW_PATH}/support_tickets.csv")

# # -------------------------------------------------
# # FIX 1: SAFE STRING IDS (CRITICAL FOR POWER BI)
# # -------------------------------------------------

# customers["customer_id"] = customers["customer_id"].astype(str).str.strip()
# transactions["customer_id"] = transactions["customer_id"].astype(str).str.strip()
# tickets["customer_id"] = tickets["customer_id"].astype(str).str.strip()

# # -------------------------------------------------
# # FIX 2: REMOVE DUPLICATE CUSTOMERS (IMPORTANT FIX YOU ASKED)
# # -------------------------------------------------

# customers = customers.drop_duplicates(subset=["customer_id"])

# # -------------------------------------------------
# # FIX 3: PARSE DATES SAFELY
# # -------------------------------------------------

# customers["acquisition_date"] = pd.to_datetime(customers["acquisition_date"], errors="coerce")
# transactions["month"] = pd.to_datetime(transactions["month"], errors="coerce")
# tickets["open_date"] = pd.to_datetime(tickets["open_date"], errors="coerce")
# tickets["close_date"] = pd.to_datetime(tickets["close_date"], errors="coerce")

# # -------------------------------------------------
# # FIX 4: TRANSACTIONS CLEANING
# # -------------------------------------------------

# transactions = transactions.drop_duplicates()

# transactions["amount"] = pd.to_numeric(transactions["amount"], errors="coerce")
# transactions["amount"] = transactions["amount"].fillna(transactions["amount"].median())

# transactions = transactions[transactions["month"].notna()]

# # -------------------------------------------------
# # FIX 5: CATEGORICAL CLEANING
# # -------------------------------------------------

# customers["segment"] = customers["segment"].astype(str).str.title()
# customers["region"] = customers["region"].astype(str).str.upper()

# # -------------------------------------------------
# # FIX 6: MRR CLEANING
# # -------------------------------------------------

# customers["mrr"] = pd.to_numeric(customers["mrr"], errors="coerce")
# customers["mrr"] = customers["mrr"].fillna(customers["mrr"].median())

# # -------------------------------------------------
# # FIX 7: SUPPORT TICKETS VALIDATION
# # -------------------------------------------------

# tickets = tickets.dropna(subset=["open_date", "close_date"])
# tickets = tickets[tickets["close_date"] >= tickets["open_date"]]

# # -------------------------------------------------
# # SAVE CLEAN FILES
# # -------------------------------------------------

# customers.to_csv(f"{CLEAN_PATH}/customers_clean.csv", index=False)
# transactions.to_csv(f"{CLEAN_PATH}/transactions_clean.csv", index=False)
# tickets.to_csv(f"{CLEAN_PATH}/support_tickets_clean.csv", index=False)

# # -------------------------------------------------
# # SUMMARY
# # -------------------------------------------------

# logging.info("Cleaning completed successfully")
# logging.info(f"Customers: {customers.shape}")
# logging.info(f"Transactions: {transactions.shape}")
# logging.info(f"Tickets: {tickets.shape}")
# logging.info(f"Saved to: {CLEAN_PATH}")


"""
Data Cleaning Pipeline — Customer Revenue & Support Analysis
FINAL VERSION (Power BI + SQL safe)

Fixes:
- Duplicate rows
- Data types
- Missing values
- Invalid dates
- Category normalization
"""

import pandas as pd
import numpy as np
import os

os.makedirs("data/clean", exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
customers = pd.read_csv("data/raw/customers.csv")
transactions = pd.read_csv("data/raw/transactions.csv")
tickets = pd.read_csv("data/raw/support_tickets.csv")

# -----------------------------
# CUSTOMERS CLEANING
# -----------------------------

customers["segment"] = customers["segment"].str.title()
customers["mrr"] = pd.to_numeric(customers["mrr"], errors="coerce")
customers["mrr"] = customers.groupby("segment")["mrr"].transform(
    lambda x: x.fillna(x.median())
)

# -----------------------------
# TRANSACTIONS CLEANING
# -----------------------------

transactions = transactions.drop_duplicates()

transactions["amount"] = pd.to_numeric(transactions["amount"], errors="coerce")
transactions["amount"] = transactions["amount"].fillna(transactions["amount"].median())

# convert month → proper date (for Power BI)
transactions["transaction_date"] = pd.to_datetime(
    transactions["month"] + "-01"
)

# -----------------------------
# SUPPORT TICKETS CLEANING
# -----------------------------

tickets["open_date"] = pd.to_datetime(tickets["open_date"])
tickets["close_date"] = pd.to_datetime(tickets["close_date"])

invalid = tickets["close_date"] < tickets["open_date"]
tickets.loc[invalid, "close_date"] = tickets.loc[invalid, "open_date"] + pd.Timedelta(days=1)

# -----------------------------
# SAVE CLEAN DATA
# -----------------------------
customers.to_csv("data/clean/customers_clean.csv", index=False)
transactions.to_csv("data/clean/transactions_clean.csv", index=False)
tickets.to_csv("data/clean/support_tickets_clean.csv", index=False)

print("Cleaning completed successfully")
print(customers.shape, transactions.shape, tickets.shape)