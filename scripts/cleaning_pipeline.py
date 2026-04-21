"""
data_cleaning.py

Clean raw SaaS dataset.

Tasks:
- remove duplicates
- fix inconsistent labels
- handle missing values
- fix impossible dates
"""

import pandas as pd
import os

# load data

customers = pd.read_csv("data/raw/customers.csv")
transactions = pd.read_csv("data/raw/transactions.csv")
tickets = pd.read_csv("data/raw/support_tickets.csv")

# --------------------------------------------------
# Fix segment labels
# --------------------------------------------------

customers["segment"] = customers["segment"].str.lower()

segment_map = {
    "enterprise": "enterprise",
    "mid-market": "mid-market",
    "smb": "smb",
    "smb ": "smb",
    "smbs": "smb"
}

customers["segment"] = customers["segment"].replace(segment_map)

# --------------------------------------------------
# Remove duplicates
# --------------------------------------------------

customers = customers.drop_duplicates(subset="customer_id")

# --------------------------------------------------
# Fix missing MRR
# --------------------------------------------------

customers["mrr"] = customers["mrr"].fillna(
    customers.groupby("segment")["mrr"].transform("median")
)

# --------------------------------------------------
# Fix impossible transaction dates
# --------------------------------------------------

transactions["month"] = pd.to_datetime(transactions["month"], errors="coerce")

transactions = transactions[
    transactions["month"] < pd.Timestamp.today()
]

# --------------------------------------------------
# Fix missing CSAT
# --------------------------------------------------

tickets["csat_score"] = tickets["csat_score"].fillna(
    tickets["csat_score"].median()
)

# --------------------------------------------------
# Save cleaned data
# --------------------------------------------------

os.makedirs("data/clean", exist_ok=True)

customers.to_csv("data/clean/customers_clean.csv", index=False)
transactions.to_csv("data/clean/transactions_clean.csv", index=False)
tickets.to_csv("data/clean/support_tickets_clean.csv", index=False)

print("Cleaning completed")
print("customers:", customers.shape)
print("transactions:", transactions.shape)
print("tickets:", tickets.shape)