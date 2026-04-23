
"""
Data Cleaning Pipeline
Customer Revenue & Support Analysis

This script:
1. Loads raw CSV files
2. Detects and fixes data quality issues
3. Saves clean datasets to data/clean/

Fixes applied:
1. Remove duplicate rows
2. Fix incorrect data types
3. Fix impossible dates
4. Standardize category labels
5. Handle missing values (pattern-based)

Output:
data/clean/customers_clean.csv
data/clean/transactions_clean.csv
data/clean/support_tickets_clean.csv
"""

import os
import pandas as pd
import logging

# -------------------------------------------------
# Setup logging
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------
# Paths
# -------------------------------------------------

RAW_PATH = "data/raw/"
CLEAN_PATH = "data/clean/"

os.makedirs(CLEAN_PATH, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------

def load_data():
    logging.info("Loading raw datasets...")

    customers = pd.read_csv(RAW_PATH + "customers.csv")
    transactions = pd.read_csv(RAW_PATH + "transactions.csv")
    tickets = pd.read_csv(RAW_PATH + "support_tickets.csv")

    logging.info(f"Customers: {customers.shape}")
    logging.info(f"Transactions: {transactions.shape}")
    logging.info(f"Tickets: {tickets.shape}")

    return customers, transactions, tickets


# -------------------------------------------------
# Clean Customers
# -------------------------------------------------

def clean_customers(df):
    logging.info("Cleaning customers dataset...")

    # 1. Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset="customer_id")
    logging.info(f"Removed {before - len(df)} duplicate rows")

    # 2. Standardize segment labels
    df["segment"] = df["segment"].str.lower().str.strip()

    mapping = {
        "enterprise": "enterprise",
        "mid-market": "mid-market",
        "smb": "smb"
    }

    df["segment"] = df["segment"].replace(mapping)

    # 3. Fix missing MRR (pattern-based issue)
    df["mrr"] = pd.to_numeric(df["mrr"], errors="coerce")

    # Fill missing MRR using segment median
    df["mrr"] = df.groupby("segment")["mrr"].transform(
        lambda x: x.fillna(x.median())
    )

    # 4. Convert acquisition_date to datetime
    df["acquisition_date"] = pd.to_datetime(
        df["acquisition_date"],
        errors="coerce"
    )

    return df


# -------------------------------------------------
# Clean Transactions
# -------------------------------------------------

def clean_transactions(df):
    logging.info("Cleaning transactions dataset...")

    # 1. Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    logging.info(f"Removed {before - len(df)} duplicate rows")

    # 2. Fix data type issue (string → numeric)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # 3. Handle missing values (important for BI)
    missing = df["amount"].isna().sum()
    logging.info(f"Found {missing} missing amount values")

    # Fill missing revenue with 0
    df["amount"] = df["amount"].fillna(0)

    # 4. Ensure month format is consistent (YYYY-MM)
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df["month"] = df["month"].dt.strftime("%Y-%m")

    return df


# -------------------------------------------------
# Clean Support Tickets
# -------------------------------------------------

def clean_tickets(df):
    logging.info("Cleaning support tickets dataset...")

    # Convert dates
    df["open_date"] = pd.to_datetime(df["open_date"], errors="coerce")
    df["close_date"] = pd.to_datetime(df["close_date"], errors="coerce")

    # 1. Fix impossible dates (close before open)
    invalid = df["close_date"] < df["open_date"]
    logging.warning(f"Found {invalid.sum()} invalid date rows")

    # Fix by setting close_date = open_date
    df.loc[invalid, "close_date"] = df.loc[invalid, "open_date"]

    # 2. Fix CSAT type
    df["csat_score"] = pd.to_numeric(df["csat_score"], errors="coerce")

    # 3. Handle missing CSAT
    df["csat_score"] = df["csat_score"].fillna(
        df["csat_score"].median()
    )

    return df


# -------------------------------------------------
# Validation
# -------------------------------------------------

def validate_data(customers, transactions, tickets):
    logging.info("Running validation checks...")

    assert customers["customer_id"].is_unique, "Duplicate customers found"
    assert transactions["amount"].isna().sum() == 0, "Amount still has NULLs"
    assert (tickets["close_date"] >= tickets["open_date"]).all(), "Invalid dates remain"

    logging.info("All validation checks passed")


# -------------------------------------------------
# Save cleaned data
# -------------------------------------------------

def save_data(customers, transactions, tickets):
    customers.to_csv(CLEAN_PATH + "customers_clean.csv", index=False)
    transactions.to_csv(CLEAN_PATH + "transactions_clean.csv", index=False)
    tickets.to_csv(CLEAN_PATH + "support_tickets_clean.csv", index=False)

    logging.info("Clean data saved to data/clean/")


# -------------------------------------------------
# Main
# -------------------------------------------------

def main():
    logging.info("Starting data cleaning pipeline")

    customers, transactions, tickets = load_data()

    customers = clean_customers(customers)
    transactions = clean_transactions(transactions)
    tickets = clean_tickets(tickets)

    validate_data(customers, transactions, tickets)

    save_data(customers, transactions, tickets)

    logging.info("Data cleaning completed successfully")


if __name__ == "__main__":
    main()