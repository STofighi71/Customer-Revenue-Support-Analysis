# SaaS Business Intelligence Project

## Overview

This project demonstrates a complete end-to-end analytics workflow for a SaaS business environment.
It includes synthetic data generation, data cleaning, SQL analysis, and an interactive Power BI dashboard.

The goal of the project is to simulate how a data analyst might analyze revenue, customer behavior, and support performance in a subscription-based software company.

---

# Project Structure

```
project/
│
├── data/
│   ├── raw/
│   └── clean/
│
├── docs/
│   └── cleaning_report.md
│
├── scripts/
│   ├── data_generation.py
│   ├── cleaning_pipeline.py
│   └── load_to_sqlite.py
│
├── sql/
│   └── queries.sql
│
├── dashboard/
│   └── saas_dashboard.pbix
│
└── README.md
```

---

# Step 1 — Data Generation

Synthetic datasets were generated to simulate a SaaS company environment.

The following datasets were created:

### customers

Contains customer information including:

* customer_id
* company_name
* segment
* acquisition_date
* MRR

### transactions

Simulates financial events such as subscriptions and churn.

Columns include:

* customer_id
* month
* transaction_type
* amount

### support_tickets

Contains simulated customer support interactions.

Columns include:

* ticket_id
* customer_id
* open_date
* channel
* csat_score

The generated datasets are stored in:

```
data/raw/
```

---

# Step 2 — Data Cleaning

A cleaning script was used to:

• remove missing values
• standardize date formats
• ensure numeric columns are valid
• export cleaned datasets

Clean data is stored in:

```
data/clean/
```

---

# Step 3 — SQL Analysis

Clean datasets were loaded into SQLite.

Eight SQL queries were written to answer business questions such as:

1. Total MRR by customer segment
2. Top customers by revenue
3. Month-over-month revenue growth
4. Monthly churn
5. Average CSAT by support channel
6. Support ticket volume per customer
7. Cohort revenue by signup quarter
8. High-support customers before churn

These queries are stored in:

```
sql/queries.sql
```

---

# Step 4 — Power BI Dashboard

An interactive dashboard was created using Power BI.

The dashboard contains three pages:

---

## Executive Summary

Key SaaS metrics:

• Monthly Recurring Revenue (MRR)
• Annual Recurring Revenue (ARR)
• Average Revenue Per Account (ARPA)
• Net Revenue Retention (NRR)
• Logo Churn Rate

A time-series chart visualizes revenue growth.

---

## Customer Overview

Provides insight into the customer base:

• Customer table with revenue and CSAT
• Customer distribution by segment
• Relationship between revenue and support load

---

## Support Analysis

Focuses on customer support performance:

• Monthly ticket volume
• Resolution time by priority
• CSAT score distribution
• Support channel performance

---

# Tools Used

* Python
* SQLite
* Power BI
* SQL

---

# Key Skills Demonstrated

* Data generation
* Data cleaning
* SQL analytics
* SaaS metrics analysis
* BI dashboard design
* End-to-end data workflow


