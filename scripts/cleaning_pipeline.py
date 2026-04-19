"""
Data Cleaning Pipeline
Customer Revenue & Support Analysis

This script cleans the raw datasets generated in Step 1.

Tasks performed:
- Load raw datasets
- Detect and fix the five intentional data quality issues
- Validate cleaned data
- Save cleaned datasets

Input:
data/raw/

Output:
data/clean/
"""

import pandas as pd
import logging
from pathlib import Path


# -------------------------------------------------
# Logging configuration
# -------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# -------------------------------------------------
# Paths
# -------------------------------------------------

RAW_PATH = Path("data/raw")
CLEAN_PATH = Path("data/clean")

CLEAN_PATH.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# Load datasets
# -------------------------------------------------

def load_data():

    logger.info("Loading raw datasets...")

    customers = pd.read_csv(RAW_PATH / "customers.csv")
    transactions = pd.read_csv(RAW_PATH / "transactions.csv")
    tickets = pd.read_csv(RAW_PATH / "support_tickets.csv")

    logger.info(f"Customers shape: {customers.shape}")
    logger.info(f"Transactions shape: {transactions.shape}")
    logger.info(f"Support tickets shape: {tickets.shape}")

    return customers, transactions, tickets


# -------------------------------------------------
# Clean customers dataset
# -------------------------------------------------

def clean_customers(df):

    logger.info("Cleaning customers dataset...")

    # Convert acquisition_date to datetime
    df["acquisition_date"] = pd.to_datetime(
        df["acquisition_date"],
        errors="coerce"
    )

    # -------------------------------------------------
    # FIX ISSUE 4
    # Inconsistent segment labels
    # enterprise / ENTERPRISE -> Enterprise
    # -------------------------------------------------

    df["segment"] = df["segment"].str.lower().str.title()

    # -------------------------------------------------
    # FIX ISSUE 5
    # Pattern-based missing values in MRR for SMB
    # Replace missing values with median MRR of SMB
    # -------------------------------------------------

    smb_median = df.loc[df["segment"] == "Smb", "mrr"].median()

    df.loc[
        (df["segment"] == "Smb") & (df["mrr"].isna()),
        "mrr"
    ] = smb_median

    return df


# -------------------------------------------------
# Clean transactions dataset
# -------------------------------------------------

def clean_transactions(df):

    logger.info("Cleaning transactions dataset...")

    # -------------------------------------------------
    # FIX ISSUE 1
    # Remove exact duplicate rows
    # -------------------------------------------------

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    logger.info(f"Removed {before - after} duplicate rows")

    # -------------------------------------------------
    # FIX ISSUE 2
    # Wrong data type in amount column
    # -------------------------------------------------

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Convert month column to datetime
    df["month"] = pd.to_datetime(
        df["month"],
        format="%Y-%m",
        errors="coerce"
    )

    return df


# -------------------------------------------------
# Clean support tickets dataset
# -------------------------------------------------

def clean_tickets(df):

    logger.info("Cleaning support tickets dataset...")

    df["open_date"] = pd.to_datetime(df["open_date"])
    df["close_date"] = pd.to_datetime(df["close_date"])

    # -------------------------------------------------
    # FIX ISSUE 3
    # Impossible date relationship
    # close_date earlier than open_date
    # -------------------------------------------------

    invalid_dates = df["close_date"] < df["open_date"]

    count_invalid = invalid_dates.sum()

    if count_invalid > 0:

        logger.warning(f"Found {count_invalid} impossible ticket dates")

        df.loc[
            invalid_dates,
            "close_date"
        ] = df.loc[
            invalid_dates,
            "open_date"
        ]

    return df


# -------------------------------------------------
# Validation checks
# -------------------------------------------------

def validate_data(customers, transactions, tickets):

    logger.info("Running validation checks...")

    assert customers["customer_id"].is_unique, \
        "Customer IDs must be unique"

    assert transactions["amount"].notna().all(), \
        "Amount column contains null values"

    assert (
        tickets["close_date"] >= tickets["open_date"]
    ).all(), \
        "Ticket date validation failed"

    logger.info("All validation checks passed")


# -------------------------------------------------
# Save cleaned datasets
# -------------------------------------------------

def save_data(customers, transactions, tickets):

    customers.to_csv(
        CLEAN_PATH / "customers_clean.csv",
        index=False
    )

    transactions.to_csv(
        CLEAN_PATH / "transactions_clean.csv",
        index=False
    )

    tickets.to_csv(
        CLEAN_PATH / "support_tickets_clean.csv",
        index=False
    )

    logger.info("Cleaned datasets saved to data/clean")


# -------------------------------------------------
# Main pipeline
# -------------------------------------------------

def main():

    logger.info("Starting data cleaning pipeline")

    customers, transactions, tickets = load_data()

    customers = clean_customers(customers)

    transactions = clean_transactions(transactions)

    tickets = clean_tickets(tickets)

    validate_data(
        customers,
        transactions,
        tickets
    )

    save_data(
        customers,
        transactions,
        tickets
    )

    logger.info("Data cleaning pipeline completed successfully")


if __name__ == "__main__":
    main()