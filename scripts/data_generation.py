
# """
# Data Generation Script — Customer Revenue & Support Analysis
# FINAL STABLE VERSION (Faker-safe + Power BI compatible)

# Fixes:
# - Uses datetime.date objects (no Faker ParseError)
# - All dates within 2023–2024
# - Consistent schema for SQL + Power BI
# """

# import os
# import random
# import numpy as np
# import pandas as pd
# from faker import Faker
# from datetime import date, timedelta

# # -----------------------------
# # Setup
# # -----------------------------
# random.seed(42)
# np.random.seed(42)
# fake = Faker()
# Faker.seed(42)

# os.makedirs("data/raw", exist_ok=True)

# # -----------------------------
# # CONSTANTS
# # -----------------------------
# segments = ["SMB", "Mid-Market", "Enterprise"]
# regions = ["EMEA", "North America", "APAC", "LATAM"]
# industries = ["Finance", "Healthcare", "Retail", "Logistics", "EdTech", "SaaS", "Manufacturing", "Media"]
# transaction_types = ["new", "expansion", "contraction", "churn"]
# priorities = ["low", "medium", "high", "critical"]
# channels = ["email", "chat", "phone", "self-service"]

# # -----------------------------
# # CUSTOMERS
# # -----------------------------
# customers = []

# for i in range(1, 201):
#     customers.append({
#         "customer_id": i,
#         "company_name": fake.company(),
#         "segment": random.choice(segments),
#         "region": random.choice(regions),
#         "industry": random.choice(industries),
#         "acquisition_date": fake.date_between(date(2023, 1, 1), date(2023, 12, 31)),
#         "contract_type": random.choice(["monthly", "annual"]),
#         "csm_name": fake.name(),
#         "mrr": random.randint(1000, 50000)
#     })

# customers = pd.DataFrame(customers)

# # -----------------------------
# # TRANSACTIONS
# # -----------------------------
# transactions = []

# for i in range(1, 501):
#     transactions.append({
#         "transaction_id": i,
#         "customer_id": random.randint(1, 200),
#         "month": fake.date_between(date(2023, 1, 1), date(2024, 12, 1)).strftime("%Y-%m"),
#         "transaction_type": random.choice(transaction_types),
#         "amount": random.randint(500, 10000)
#     })

# transactions = pd.DataFrame(transactions)

# # intentional duplicate (data quality issue)
# transactions = pd.concat([transactions, transactions.iloc[[10]]], ignore_index=True)

# # -----------------------------
# # SUPPORT TICKETS
# # -----------------------------
# tickets = []

# for i in range(1, 301):
#     open_date = fake.date_between(date(2023, 1, 1), date(2024, 12, 1))

#     tickets.append({
#         "ticket_id": i,
#         "customer_id": random.randint(1, 200),
#         "open_date": open_date,
#         "close_date": open_date + timedelta(days=random.randint(1, 10)),
#         "priority": random.choice(priorities),
#         "channel": random.choice(channels),
#         "csat_score": random.randint(1, 5)
#     })

# tickets = pd.DataFrame(tickets)

# # -----------------------------
# # SAVE FILES
# # -----------------------------
# customers.to_csv("data/raw/customers.csv", index=False)
# transactions.to_csv("data/raw/transactions.csv", index=False)
# tickets.to_csv("data/raw/support_tickets.csv", index=False)

# print("Data generation completed successfully")
# print(customers.shape, transactions.shape, tickets.shape)


import pandas as pd
from datetime import datetime, timedelta
import uuid

START = datetime(2023,1,1)

# =========================
# CUSTOMERS (200)
# =========================
customers = []

for i in range(200):

    # realistic but deterministic distributions
    if i % 10 < 5:
        segment = "SMB"
    elif i % 10 < 8:
        segment = "Mid-Market"
    else:
        segment = "Enterprise"

    if i % 10 < 4:
        region = "EMEA"
    elif i % 10 < 7:
        region = "North America"
    elif i % 10 < 9:
        region = "APAC"
    else:
        region = "LATAM"

    customers.append({
        "customer_id": f"C{i:04d}",
        "company_name": f"Company_{i}",
        "segment": segment,
        "region": region,
        "industry": ["Finance","Healthcare","Retail","Logistics","EdTech","SaaS","Energy","Manufacturing"][i%8],
        "acquisition_date": START + timedelta(days=i),
        "contract_type": "monthly" if i % 3 != 0 else "annual",
        "csm_name": f"CSM_{i%8}",
        "mrr": 200 + (i%30)*80
    })

customers = pd.DataFrame(customers)

# ISSUE 1 — inconsistent labels
customers.loc[customers["segment"]=="Enterprise","segment"]="enterprise"

# ISSUE 2 — patterned missing
customers.loc[customers["segment"]=="SMB","csm_name"]=None


# =========================
# TRANSACTIONS (500)
# =========================
transactions = []

for i in range(500):
    d = START + timedelta(days=i)

    if i % 20 < 10:
        ttype = "new"
    elif i % 20 < 15:
        ttype = "expansion"
    elif i % 20 < 18:
        ttype = "contraction"
    else:
        ttype = "churn"

    transactions.append({
        "transaction_id": str(uuid.uuid4()),
        "customer_id": f"C{i%200:04d}",
        "month": d.strftime("%Y-%m"),
        "transaction_type": ttype,
        "amount": 100 + (i%25)*40
    })

transactions = pd.DataFrame(transactions)

# ISSUE 3 — wrong datatype
transactions["amount"] = transactions["amount"].astype(object)
mask = transactions["transaction_type"]=="expansion"
transactions.loc[mask,"amount"] = transactions.loc[mask,"amount"].astype(str)


# =========================
# SUPPORT TICKETS (300)
# =========================
tickets = []

for i in range(300):
    open_date = START + timedelta(days=i)

    # skewed priority
    if i % 10 < 5:
        priority="low"
    elif i % 10 < 8:
        priority="medium"
    elif i % 10 < 9:
        priority="high"
    else:
        priority="critical"

    # skewed channel
    if i % 10 < 5:
        channel="email"
    elif i % 10 < 8:
        channel="chat"
    elif i % 10 < 9:
        channel="phone"
    else:
        channel="self-service"

    # skewed CSAT
    if i % 10 < 1:
        csat=1
    elif i % 10 < 3:
        csat=2
    elif i % 10 < 5:
        csat=3
    elif i % 10 < 8:
        csat=4
    else:
        csat=5

    tickets.append({
        "ticket_id": str(uuid.uuid4()),
        "customer_id": f"C{i%200:04d}",
        "open_date": open_date,
        "close_date": open_date + timedelta(days=2),
        "priority": priority,
        "channel": channel,
        "csat_score": csat
    })

tickets = pd.DataFrame(tickets)

# ISSUE 4 — duplicates
tickets = pd.concat([tickets, tickets.iloc[:5]])

# ISSUE 5 — impossible date
mask = tickets["priority"]=="critical"
tickets.loc[mask,"close_date"] = tickets.loc[mask,"open_date"] - timedelta(days=1)


# =========================
# FORCE QUERY 8
# =========================
target="C0005"

transactions = pd.concat([transactions, pd.DataFrame([{
    "transaction_id":str(uuid.uuid4()),
    "customer_id":target,
    "month":"2024-06",
    "transaction_type":"churn",
    "amount":800
}])])

for i in range(5):
    tickets = pd.concat([tickets, pd.DataFrame([{
        "ticket_id":str(uuid.uuid4()),
        "customer_id":target,
        "open_date":datetime(2024,5,15),
        "close_date":datetime(2024,5,16),
        "priority":"high",
        "channel":"email",
        "csat_score":2
    }])])

customers.to_csv("data/raw/customers.csv",index=False)
transactions.to_csv("data/raw/transactions.csv",index=False)
tickets.to_csv("data/raw/support_tickets.csv",index=False)