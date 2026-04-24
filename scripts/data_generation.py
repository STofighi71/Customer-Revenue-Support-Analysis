
"""
Data Generation Script — Customer Revenue & Support Analysis
FINAL STABLE VERSION (Faker-safe + Power BI compatible)

Fixes:
- Uses datetime.date objects (no Faker ParseError)
- All dates within 2023–2024
- Consistent schema for SQL + Power BI
"""

import os
import random
import numpy as np
import pandas as pd
from faker import Faker
from datetime import date, timedelta

# -----------------------------
# Setup
# -----------------------------
random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

os.makedirs("data/raw", exist_ok=True)

# -----------------------------
# CONSTANTS
# -----------------------------
segments = ["SMB", "Mid-Market", "Enterprise"]
regions = ["EMEA", "North America", "APAC", "LATAM"]
industries = ["Finance", "Healthcare", "Retail", "Logistics", "EdTech", "SaaS", "Manufacturing", "Media"]
transaction_types = ["new", "expansion", "contraction", "churn"]
priorities = ["low", "medium", "high", "critical"]
channels = ["email", "chat", "phone", "self-service"]

# -----------------------------
# CUSTOMERS
# -----------------------------
customers = []

for i in range(1, 201):
    customers.append({
        "customer_id": i,
        "company_name": fake.company(),
        "segment": random.choice(segments),
        "region": random.choice(regions),
        "industry": random.choice(industries),
        "acquisition_date": fake.date_between(date(2023, 1, 1), date(2023, 12, 31)),
        "contract_type": random.choice(["monthly", "annual"]),
        "csm_name": fake.name(),
        "mrr": random.randint(1000, 50000)
    })

customers = pd.DataFrame(customers)

# -----------------------------
# TRANSACTIONS
# -----------------------------
transactions = []

for i in range(1, 501):
    transactions.append({
        "transaction_id": i,
        "customer_id": random.randint(1, 200),
        "month": fake.date_between(date(2023, 1, 1), date(2024, 12, 1)).strftime("%Y-%m"),
        "transaction_type": random.choice(transaction_types),
        "amount": random.randint(500, 10000)
    })

transactions = pd.DataFrame(transactions)

# intentional duplicate (data quality issue)
transactions = pd.concat([transactions, transactions.iloc[[10]]], ignore_index=True)

# -----------------------------
# SUPPORT TICKETS
# -----------------------------
tickets = []

for i in range(1, 301):
    open_date = fake.date_between(date(2023, 1, 1), date(2024, 12, 1))

    tickets.append({
        "ticket_id": i,
        "customer_id": random.randint(1, 200),
        "open_date": open_date,
        "close_date": open_date + timedelta(days=random.randint(1, 10)),
        "priority": random.choice(priorities),
        "channel": random.choice(channels),
        "csat_score": random.randint(1, 5)
    })

tickets = pd.DataFrame(tickets)

# -----------------------------
# SAVE FILES
# -----------------------------
customers.to_csv("data/raw/customers.csv", index=False)
transactions.to_csv("data/raw/transactions.csv", index=False)
tickets.to_csv("data/raw/support_tickets.csv", index=False)

print("Data generation completed successfully")
print(customers.shape, transactions.shape, tickets.shape)