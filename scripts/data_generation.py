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