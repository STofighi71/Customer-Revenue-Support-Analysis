"""
Data Generation Script
Customer Revenue & Support Analysis

This script generates three CSV files simulating customer, revenue,
and support activity data for a fictional SaaS company (Novelus).

Datasets generated:
- customers.csv (200 rows)
- transactions.csv (500 rows + 1 duplicate row intentionally inserted)
- support_tickets.csv (300 rows)

The script intentionally embeds FIVE data quality issues
to simulate common real-world data problems.

Issues included:
1. Exact duplicate rows
2. Incorrect data type in a column
3. Impossible date relationship
4. Inconsistent category labels
5. Pattern-based missing values

Output directory:
data/raw/
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta


# -------------------------------------------------
# Reproducibility
# -------------------------------------------------

random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)


# -------------------------------------------------
# Ensure output directory exists
# -------------------------------------------------

os.makedirs("data/raw", exist_ok=True)


# -------------------------------------------------
# Helper lists
# -------------------------------------------------

segments = ["SMB", "Mid-Market", "Enterprise"]

regions = [
    "EMEA",
    "North America",
    "APAC",
    "LATAM"
]

industries = [
    "Finance",
    "Healthcare",
    "Retail",
    "Logistics",
    "EdTech",
    "SaaS",
    "Manufacturing",
    "Media"
]

contract_types = ["monthly", "annual"]

csm_names = [
    "Alice Johnson",
    "Brian Smith",
    "Carla Gomez",
    "David Lee",
    "Emma Brown"
]

transaction_types = [
    "new",
    "expansion",
    "contraction",
    "churn"
]

priorities = [
    "low",
    "medium",
    "high",
    "critical"
]

channels = [
    "email",
    "chat",
    "phone",
    "self-service"
]


# -------------------------------------------------
# Generate customers dataset
# -------------------------------------------------

customers = []

for i in range(1, 201):

    acquisition_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    customers.append({
        "customer_id": i,
        "company_name": fake.company(),
        "segment": random.choice(segments),
        "region": random.choice(regions),
        "industry": random.choice(industries),
        "acquisition_date": acquisition_date,
        "contract_type": random.choice(contract_types),
        "csm_name": random.choice(csm_names),
        "mrr": random.randint(1000, 50000)
    })

customers = pd.DataFrame(customers)


# =================================================
# DATA QUALITY ISSUE 4
# Inconsistent category labels
# Same segment written with different capitalization
# =================================================

customers.loc[3, "segment"] = "enterprise"
customers.loc[7, "segment"] = "ENTERPRISE"


# =================================================
# DATA QUALITY ISSUE 5
# Pattern-based missing values
# MRR is missing for all SMB customers
# =================================================

customers.loc[customers["segment"] == "SMB", "mrr"] = np.nan


# -------------------------------------------------
# Generate transactions dataset
# -------------------------------------------------

transactions = []

months = pd.date_range(
    start=datetime.today() - timedelta(days=730),
    periods=24,
    freq="ME"
)

for i in range(1, 501):

    transactions.append({
        "transaction_id": i,
        "customer_id": random.randint(1, 200),
        "month": random.choice(months).strftime("%Y-%m"),
        "transaction_type": random.choice(transaction_types),
        "amount": random.randint(500, 10000)
    })

transactions = pd.DataFrame(transactions)


# =================================================
# DATA QUALITY ISSUE 2
# Incorrect data type
# One value stored as string instead of numeric
# =================================================

transactions["amount"] = transactions["amount"].astype(object)

transactions.loc[5, "amount"] = "1500"


# =================================================
# DATA QUALITY ISSUE 1
# Exact duplicate row inserted
# Simulates data ingestion duplication
# =================================================

transactions = pd.concat(
    [transactions, transactions.iloc[[10]]],
    ignore_index=True
)


# -------------------------------------------------
# Generate support tickets dataset
# -------------------------------------------------

tickets = []

for i in range(1, 301):

    open_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    close_date = open_date + timedelta(
        days=random.randint(1, 10)
    )

    tickets.append({
        "ticket_id": i,
        "customer_id": random.randint(1, 200),
        "open_date": open_date,
        "close_date": close_date,
        "priority": random.choice(priorities),
        "channel": random.choice(channels),
        "csat_score": random.randint(1, 5)
    })

tickets = pd.DataFrame(tickets)


# =================================================
# DATA QUALITY ISSUE 3
# Impossible date relationship
# Ticket closed before it was opened
# =================================================

tickets.loc[3, "close_date"] = (
    tickets.loc[3, "open_date"] - timedelta(days=2)
)


# -------------------------------------------------
# Save datasets
# -------------------------------------------------

customers.to_csv(
    "data/raw/customers.csv",
    index=False
)

transactions.to_csv(
    "data/raw/transactions.csv",
    index=False
)

tickets.to_csv(
    "data/raw/support_tickets.csv",
    index=False
)


# -------------------------------------------------
# Summary output
# -------------------------------------------------

print("\nData generation completed.\n")

print("customers.csv shape:", customers.shape)
print("transactions.csv shape:", transactions.shape)
print("support_tickets.csv shape:", tickets.shape)

print("\nFiles saved to: data/raw/")