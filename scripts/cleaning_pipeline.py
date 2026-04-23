"""
Cleaning Pipeline
Customer Revenue & Support Analysis

This script:
- Loads raw CSV files
- Detects and fixes 5 intentional data quality issues
- Produces clean datasets for analysis (Power BI + SQL)
- Does NOT modify raw files
"""

import os
import pandas as pd
import numpy as np
import logging

# -------------------------------------------------
# Setup
# -------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

RAW_PATH = "data/raw"
CLEAN_PATH = "data/clean"

os.makedirs(CLEAN_PATH, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------

logging.info("Loading raw datasets...")

customers = pd.read_csv(f"{RAW_PATH}/customers.csv")
transactions = pd.read_csv(f"{RAW_PATH}/transactions.csv")
tickets = pd.read_csv(f"{RAW_PATH}/support_tickets.csv")

# -------------------------------------------------
# Convert date columns
# -------------------------------------------------

customers["acquisition_date"] = pd.to_datetime(customers["acquisition_date"], errors="coerce")
transactions["month"] = pd.to_datetime(transactions["month"], errors="coerce", format="%m/%d/%Y")
tickets["open_date"] = pd.to_datetime(tickets["open_date"], errors="coerce")
tickets["close_date"] = pd.to_datetime(tickets["close_date"], errors="coerce")

# -------------------------------------------------
# DATA ISSUE 1: Duplicate rows (transactions)
# -------------------------------------------------

transactions_before = len(transactions)
transactions = transactions.drop_duplicates()
logging.info(f"Removed {transactions_before - len(transactions)} duplicate rows")

# -------------------------------------------------
# DATA ISSUE 2: Wrong data type (amount stored as string)
# -------------------------------------------------

transactions["amount"] = pd.to_numeric(transactions["amount"], errors="coerce")

# -------------------------------------------------
# DATA ISSUE 3: Impossible dates (2099 or invalid range)
# -------------------------------------------------

max_valid_date = pd.to_datetime("today") + pd.DateOffset(days=1)

transactions = transactions[
    (transactions["month"] <= max_valid_date)
]

# -------------------------------------------------
# DATA ISSUE 4: Inconsistent category labels
# -------------------------------------------------

customers["segment"] = customers["segment"].str.title()

# -------------------------------------------------
# DATA ISSUE 5: Pattern-based missing values (SMB missing MRR)
# -------------------------------------------------

customers.loc[
    customers["segment"] == "Smb",
    "mrr"
] = customers.loc[
    customers["segment"] == "Smb",
    "mrr"
].fillna(customers["mrr"].median())

# -------------------------------------------------
# Additional safety cleanup
# -------------------------------------------------

tickets = tickets.dropna(subset=["open_date", "close_date"])

tickets = tickets[tickets["close_date"] >= tickets["open_date"]]

# -------------------------------------------------
# Save clean datasets
# -------------------------------------------------

customers.to_csv(f"{CLEAN_PATH}/customers_clean.csv", index=False)
transactions.to_csv(f"{CLEAN_PATH}/transactions_clean.csv", index=False)
tickets.to_csv(f"{CLEAN_PATH}/support_tickets_clean.csv", index=False)

# -------------------------------------------------
# Summary
# -------------------------------------------------

logging.info("Cleaning completed successfully")
logging.info(f"Customers: {customers.shape}")
logging.info(f"Transactions: {transactions.shape}")
logging.info(f"Tickets: {tickets.shape}")
logging.info(f"Saved to: {CLEAN_PATH}")