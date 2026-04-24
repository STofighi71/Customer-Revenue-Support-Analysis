# SaaS Business Intelligence Project

## Overview

This project demonstrates an end-to-end analytics workflow for a SaaS business environment. It covers data generation, cleaning, SQL-based analysis, and dashboard development in Power BI.

The objective is to simulate how a data analyst would analyze revenue performance, customer behavior, and support operations in a subscription-based business.

---

## Project Structure

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
│   └── Customer-Revenue-Support-Dashboard.pbix
│
└── README.md
```

---

## Step 1 — Data Generation

Synthetic datasets were generated using Python to simulate a SaaS business model.

### Datasets

#### customers

Contains customer-level attributes:

* customer_id
* company_name
* segment
* region
* acquisition_date
* mrr

#### transactions

Represents monthly revenue events:

* customer_id
* month
* transaction_type (new, expansion, contraction, churn)
* amount

#### support_tickets

Simulates support interactions:

* ticket_id
* customer_id
* open_date
* close_date
* priority
* channel
* csat_score

Raw datasets are stored in:

```
data/raw/
```

---

## Step 2 — Data Cleaning

A data cleaning pipeline was implemented to ensure data quality and consistency.

### Key transformations:

* Handled missing values (e.g. amount → filled with 0)
* Standardized date formats across all tables
* Removed invalid or future dates
* Ensured consistent data types
* Generated proper date fields for time-based analysis

Clean datasets are stored in:

```
data/clean/
```

---

## Step 3 — SQL Analysis

Clean data was loaded into SQLite and analyzed using SQL.

### Business Questions Answered:

1. Total MRR by customer segment
2. Top 10 customers by MRR
3. Month-over-month revenue change
4. Monthly logo churn
5. Average CSAT by support channel
6. Support ticket volume per customer per month
7. Cohort-based revenue (by signup quarter)
8. Customers with high support activity before churn

SQL queries are available in:

```
sql/queries.sql
```

---

## Step 4 — Power BI Dashboard

An interactive dashboard was developed with three pages and shared slicers (date and segment).

---

### Executive Summary

Key SaaS KPIs:

* Monthly Recurring Revenue (MRR)
* Annual Recurring Revenue (ARR)
* Average Revenue Per Account (ARPA)
* Net Revenue Retention (NRR)
* Logo Churn Rate

Each KPI displays:

* Current value
* Change vs previous month (MoM)

A time-series line chart shows MRR trend over time.

---

### Customer Overview

Provides insights into the customer base:

* Customer table including segment, region, MRR, and latest CSAT score
* Distribution of customers by segment
* Scatter plot of MRR vs. support ticket volume

---

### Support Analysis

Focuses on operational performance:

* Monthly ticket volume
* Average resolution time by priority
* CSAT score distribution
* Ticket count and average CSAT by channel

---

## Data Model

A star schema model was implemented:

* DateTable connected to:

  * transactions (transaction_date)
  * support_tickets (open_date)
* customers linked via customer_id

Time intelligence is based on monthly granularity using MonthStart.

---

## Key Metrics (Definitions)

* **MRR (Monthly Recurring Revenue)**: Sum of transaction amounts per month 
* **ARR (Annual Recurring Revenue)**: MRR × 12 
* **ARPA (Average Revenue Per Account)**: MRR / number of customers
* **Churned Customers**: Distinct customers with churn transactions
* **NRR (Net Revenue Retention)**: Ratio of non-churn revenue to total revenue (simplified)

---

## Important Notes

* This project uses synthetic data, which may not fully reflect real-world SaaS distributions.
* NRR values tend to be close to 1 due to relatively low churn impact in the generated dataset.
* Churn events are sparse and distributed, resulting in low monthly churn counts.

---

## Tools Used

* Python (data generation & cleaning)
* SQLite (SQL analysis)
* Power BI (dashboard)
* SQL

---

## Skills Demonstrated

* End-to-end data pipeline development
* Data cleaning and validation
* SQL analytics and business queries
* SaaS metric design and interpretation
* Data modeling (star schema)
* Dashboard design and storytelling

---

## Conclusion

This project demonstrates the ability to transform raw data into actionable insights through a complete analytics workflow.

It highlights both technical skills and analytical thinking required for real-world SaaS business intelligence scenarios.
