# """
# Data Generation Script
# Customer Revenue & Support Analysis

# This script generates three CSV files simulating customer, revenue,
# and support activity data for a fictional SaaS company (Novelus).

# Datasets generated:
# - customers.csv (200 rows)
# - transactions.csv (500 rows + 1 duplicate row intentionally inserted)
# - support_tickets.csv (300 rows)

# The script intentionally embeds FIVE data quality issues
# to simulate common real-world data problems.

# Issues included:
# 1. Exact duplicate rows
# 2. Incorrect data type in a column
# 3. Impossible date relationship
# 4. Inconsistent category labels
# 5. Pattern-based missing values

# Output directory:
# data/raw/
# """

# import os
# import random
# import numpy as np
# import pandas as pd
# from faker import Faker
# from datetime import datetime, timedelta


# # -------------------------------------------------
# # Reproducibility
# # -------------------------------------------------

# random.seed(42)
# np.random.seed(42)
# fake = Faker()
# Faker.seed(42)


# # -------------------------------------------------
# # Ensure output directory exists
# # -------------------------------------------------

# os.makedirs("data/raw", exist_ok=True)


# # -------------------------------------------------
# # Helper lists
# # -------------------------------------------------

# segments = ["SMB", "Mid-Market", "Enterprise"]

# regions = [
#     "EMEA",
#     "North America",
#     "APAC",
#     "LATAM"
# ]

# industries = [
#     "Finance",
#     "Healthcare",
#     "Retail",
#     "Logistics",
#     "EdTech",
#     "SaaS",
#     "Manufacturing",
#     "Media"
# ]

# contract_types = ["monthly", "annual"]

# csm_names = [
#     "Alice Johnson",
#     "Brian Smith",
#     "Carla Gomez",
#     "David Lee",
#     "Emma Brown"
# ]

# transaction_types = [
#     "new",
#     "expansion",
#     "contraction",
#     "churn"
# ]

# priorities = [
#     "low",
#     "medium",
#     "high",
#     "critical"
# ]

# channels = [
#     "email",
#     "chat",
#     "phone",
#     "self-service"
# ]


# # -------------------------------------------------
# # Generate customers dataset
# # -------------------------------------------------

# customers = []

# for i in range(1, 201):

#     acquisition_date = fake.date_between(
#         start_date="-2y",
#         end_date="today"
#     )

#     customers.append({
#         "customer_id": i,
#         "company_name": fake.company(),
#         "segment": random.choice(segments),
#         "region": random.choice(regions),
#         "industry": random.choice(industries),
#         "acquisition_date": acquisition_date,
#         "contract_type": random.choice(contract_types),
#         "csm_name": random.choice(csm_names),
#         "mrr": random.randint(1000, 50000)
#     })

# customers = pd.DataFrame(customers)


# # =================================================
# # DATA QUALITY ISSUE 4
# # Inconsistent category labels
# # Same segment written with different capitalization
# # =================================================

# customers.loc[3, "segment"] = "enterprise"
# customers.loc[7, "segment"] = "ENTERPRISE"


# # =================================================
# # DATA QUALITY ISSUE 5
# # Pattern-based missing values
# # MRR is missing for all SMB customers
# # =================================================

# customers.loc[customers["segment"] == "SMB", "mrr"] = np.nan


# # -------------------------------------------------
# # Generate transactions dataset
# # -------------------------------------------------

# transactions = []

# months = pd.date_range(
#     start=datetime.today() - timedelta(days=730),
#     periods=24,
#     freq="ME"
# )

# for i in range(1, 501):

#     transactions.append({
#         "transaction_id": i,
#         "customer_id": random.randint(1, 200),
#         "month": random.choice(months).strftime("%Y-%m"),
#         "transaction_type": random.choice(transaction_types),
#         "amount": random.randint(500, 10000)
#     })

# transactions = pd.DataFrame(transactions)


# # =================================================
# # DATA QUALITY ISSUE 2
# # Incorrect data type
# # One value stored as string instead of numeric
# # =================================================

# transactions["amount"] = transactions["amount"].astype(object)

# transactions.loc[5, "amount"] = "1500"


# # =================================================
# # DATA QUALITY ISSUE 1
# # Exact duplicate row inserted
# # Simulates data ingestion duplication
# # =================================================

# transactions = pd.concat(
#     [transactions, transactions.iloc[[10]]],
#     ignore_index=True
# )


# # -------------------------------------------------
# # Generate support tickets dataset
# # -------------------------------------------------

# tickets = []

# for i in range(1, 301):

#     open_date = fake.date_between(
#         start_date="-2y",
#         end_date="today"
#     )

#     close_date = open_date + timedelta(
#         days=random.randint(1, 10)
#     )

#     tickets.append({
#         "ticket_id": i,
#         "customer_id": random.randint(1, 200),
#         "open_date": open_date,
#         "close_date": close_date,
#         "priority": random.choice(priorities),
#         "channel": random.choice(channels),
#         "csat_score": random.randint(1, 5)
#     })

# tickets = pd.DataFrame(tickets)


# # =================================================
# # DATA QUALITY ISSUE 3
# # Impossible date relationship
# # Ticket closed before it was opened
# # =================================================

# tickets.loc[3, "close_date"] = (
#     tickets.loc[3, "open_date"] - timedelta(days=2)
# )


# # -------------------------------------------------
# # Save datasets
# # -------------------------------------------------

# customers.to_csv(
#     "data/raw/customers.csv",
#     index=False
# )

# transactions.to_csv(
#     "data/raw/transactions.csv",
#     index=False
# )

# tickets.to_csv(
#     "data/raw/support_tickets.csv",
#     index=False
# )


# # -------------------------------------------------
# # Summary output
# # -------------------------------------------------

# print("\nData generation completed.\n")

# print("customers.csv shape:", customers.shape)
# print("transactions.csv shape:", transactions.shape)
# print("support_tickets.csv shape:", tickets.shape)

# print("\nFiles saved to: data/raw/")











"""
data_generation.py

Generate synthetic SaaS dataset for the project:
Customer Revenue & Support Analysis

Tables generated:
- customers.csv
- transactions.csv
- support_tickets.csv

Data characteristics:
- realistic SaaS MRR distribution
- churn events
- support ticket spikes before churn
- intentional data quality issues
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from faker import Faker
import os

fake = Faker()

# reproducibility
np.random.seed(42)
random.seed(42)

N_CUSTOMERS = 200

# segments distribution
segments = ["enterprise", "mid-market", "smb"]
segment_probs = [0.25, 0.35, 0.40]

regions = ["North America", "Europe", "APAC"]
industries = ["SaaS", "Fintech", "Ecommerce", "Healthcare"]

contract_types = ["monthly", "annual"]

csm_names = ["Alice", "Bob", "Charlie", "Diana"]

# --------------------------------------------------
# Customers table
# --------------------------------------------------

customers = []

for i in range(N_CUSTOMERS):

    customer_id = f"C{i:04d}"

    segment = np.random.choice(segments, p=segment_probs)

    # realistic MRR distribution
    if segment == "enterprise":
        mrr = np.random.randint(5000, 20000)
    elif segment == "mid-market":
        mrr = np.random.randint(1000, 5000)
    else:
        mrr = np.random.randint(100, 1000)

    acquisition_date = fake.date_between(start_date="-2y", end_date="-6m")

    customers.append({
        "customer_id": customer_id,
        "company_name": fake.company(),
        "segment": segment,
        "region": random.choice(regions),
        "industry": random.choice(industries),
        "acquisition_date": acquisition_date,
        "contract_type": random.choice(contract_types),
        "csm_name": random.choice(csm_names),
        "mrr": mrr
    })

customers_df = pd.DataFrame(customers)

# --------------------------------------------------
# Intentional Data Issues
# --------------------------------------------------

# inconsistent labels
customers_df.loc[0:3, "segment"] = ["Enterprise", "SMB", "sMb", "MID-MARKET"]

# missing MRR pattern for SMB
mask = customers_df["segment"].str.lower() == "smb"
customers_df.loc[mask.sample(frac=0.1).index, "mrr"] = None

# duplicate rows
customers_df = pd.concat([customers_df, customers_df.iloc[:2]])

# --------------------------------------------------
# Transactions table
# --------------------------------------------------

transactions = []

start_month = datetime(2023, 1, 1)

for _, row in customers_df.iterrows():

    customer_id = row["customer_id"]
    mrr = row["mrr"]

    months_active = random.randint(4, 12)

    churn = random.random() < 0.25

    for m in range(months_active):

        month = start_month + timedelta(days=30*m)

        transactions.append({
            "transaction_id": fake.uuid4(),
            "customer_id": customer_id,
            "month": month.strftime("%Y-%m-%d"),
            "transaction_type": "recurring",
            "amount": mrr
        })

    if churn:
        churn_month = start_month + timedelta(days=30*months_active)

        transactions.append({
            "transaction_id": fake.uuid4(),
            "customer_id": customer_id,
            "month": churn_month.strftime("%Y-%m-%d"),
            "transaction_type": "churn",
            "amount": 0
        })

transactions_df = pd.DataFrame(transactions)

# impossible future date (data issue)
transactions_df.loc[5, "month"] = "2099-01-01"

# --------------------------------------------------
# Support Tickets
# --------------------------------------------------

tickets = []

channels = ["email", "chat", "phone"]
priorities = ["low", "medium", "high"]

for customer_id in customers_df["customer_id"].unique():

    n_tickets = np.random.poisson(2)

    for _ in range(n_tickets):

        open_date = fake.date_between(start_date="-1y", end_date="today")

        tickets.append({
            "ticket_id": fake.uuid4(),
            "customer_id": customer_id,
            "open_date": open_date,
            "close_date": open_date + timedelta(days=random.randint(1,5)),
            "priority": random.choice(priorities),
            "channel": random.choice(channels),
            "csat_score": random.choice([1,2,3,4,5])
        })

# --------------------------------------------------
# Ticket spikes before churn (important for Query 8)
# --------------------------------------------------

churned_customers = transactions_df[
    transactions_df["transaction_type"]=="churn"
]["customer_id"].unique()

for customer_id in random.sample(list(churned_customers), 10):

    spike_month = fake.date_between(start_date="-6m", end_date="-2m")

    for i in range(5):  # 5 tickets in same month

        tickets.append({
            "ticket_id": fake.uuid4(),
            "customer_id": customer_id,
            "open_date": spike_month,
            "close_date": spike_month + timedelta(days=2),
            "priority": "high",
            "channel": "email",
            "csat_score": random.choice([1,2])
        })

tickets_df = pd.DataFrame(tickets)

# patterned missing CSAT
tickets_df.loc[tickets_df.sample(frac=0.05).index, "csat_score"] = None

# --------------------------------------------------
# Save files
# --------------------------------------------------

os.makedirs("data/raw", exist_ok=True)

customers_df.to_csv("data/raw/customers.csv", index=False)
transactions_df.to_csv("data/raw/transactions.csv", index=False)
tickets_df.to_csv("data/raw/support_tickets.csv", index=False)

print("Data generation completed")
print("customers:", customers_df.shape)
print("transactions:", transactions_df.shape)
print("tickets:", tickets_df.shape)