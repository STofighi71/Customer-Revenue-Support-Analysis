
# """
# Data Cleaning Pipeline — Customer Revenue & Support Analysis
# FINAL VERSION (Power BI + SQL safe)

# Fixes:
# - Duplicate rows
# - Data types
# - Missing values
# - Invalid dates
# - Category normalization
# """

# import pandas as pd
# import numpy as np
# import os

# os.makedirs("data/clean", exist_ok=True)

# # -----------------------------
# # LOAD DATA
# # -----------------------------
# customers = pd.read_csv("data/raw/customers.csv")
# transactions = pd.read_csv("data/raw/transactions.csv")
# tickets = pd.read_csv("data/raw/support_tickets.csv")

# # -----------------------------
# # CUSTOMERS CLEANING
# # -----------------------------

# customers["segment"] = customers["segment"].str.title()
# customers["mrr"] = pd.to_numeric(customers["mrr"], errors="coerce")
# customers["mrr"] = customers.groupby("segment")["mrr"].transform(
#     lambda x: x.fillna(x.median())
# )

# # -----------------------------
# # TRANSACTIONS CLEANING
# # -----------------------------

# transactions = transactions.drop_duplicates()

# transactions["amount"] = pd.to_numeric(transactions["amount"], errors="coerce")
# transactions["amount"] = transactions["amount"].fillna(transactions["amount"].median())

# # convert month → proper date (for Power BI)
# transactions["transaction_date"] = pd.to_datetime(
#     transactions["month"] + "-01"
# )

# # -----------------------------
# # SUPPORT TICKETS CLEANING
# # -----------------------------

# tickets["open_date"] = pd.to_datetime(tickets["open_date"])
# tickets["close_date"] = pd.to_datetime(tickets["close_date"])

# invalid = tickets["close_date"] < tickets["open_date"]
# tickets.loc[invalid, "close_date"] = tickets.loc[invalid, "open_date"] + pd.Timedelta(days=1)

# # -----------------------------
# # SAVE CLEAN DATA
# # -----------------------------
# customers.to_csv("data/clean/customers_clean.csv", index=False)
# transactions.to_csv("data/clean/transactions_clean.csv", index=False)
# tickets.to_csv("data/clean/support_tickets_clean.csv", index=False)

# print("Cleaning completed successfully")
# print(customers.shape, transactions.shape, tickets.shape)



import pandas as pd

customers = pd.read_csv("data/raw/customers.csv")
transactions = pd.read_csv("data/raw/transactions.csv")
tickets = pd.read_csv("data/raw/support_tickets.csv")

# fix labels
customers["segment"] = customers["segment"].str.title()

# fix missing
customers["csm_name"] = customers["csm_name"].fillna("Unassigned")

# fix datatype
transactions["amount"] = pd.to_numeric(transactions["amount"], errors="coerce").fillna(0)

# remove duplicates
tickets = tickets.drop_duplicates()

# fix dates
tickets["open_date"] = pd.to_datetime(tickets["open_date"])
tickets["close_date"] = pd.to_datetime(tickets["close_date"])

mask = tickets["close_date"] < tickets["open_date"]
tickets.loc[mask,"close_date"] = tickets.loc[mask,"open_date"] + pd.Timedelta(days=2)

# create month_date for BI
transactions["month_date"] = pd.to_datetime(transactions["month"]+"-01")

# final clean
customers = customers.dropna()
transactions = transactions.dropna()
tickets = tickets.dropna()

customers.to_csv("data/clean/customers_clean.csv",index=False)
transactions.to_csv("data/clean/transactions_clean.csv",index=False)
tickets.to_csv("data/clean/support_tickets_clean.csv",index=False)