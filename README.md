
### Customer Revenue & Support Analysis

End-to-end data analytics project simulating SaaS business metrics including revenue, customer support activity, and retention analysis.

This project demonstrates the full workflow of a data analyst — from raw data generation to cleaning, SQL analysis, and building a Power BI dashboard.

---

# Project Overview

Novelus is a fictional SaaS company preparing internal analytics for strategic reporting and investor discussions.

The goal of this project is to simulate realistic business data and demonstrate the ability to:

• generate synthetic datasets
• detect and clean real-world data quality issues
• perform analytical queries using SQL
• build an executive dashboard for business insights

The project follows a structured four-step workflow.

---

# Project Workflow

## Step 1 — Data Generation (Python)

A Python script generates three datasets representing two years of simulated SaaS company activity.

Generated datasets:

customers.csv — 200 customers
transactions.csv — 500 revenue events
support_tickets.csv — 300 support interactions

The script intentionally embeds five realistic data quality issues to simulate problems commonly found in real company datasets.

Embedded issues include:

1. Duplicate rows
2. Incorrect data types
3. Impossible dates
4. Inconsistent category labels
5. Pattern-based missing values

The output is saved in the **data/raw/** directory.

---

## Step 2 — Data Cleaning (Python)

A second Python script loads the raw datasets and performs a full cleaning pipeline.

The cleaning process includes:

• detecting duplicate rows
• correcting incorrect data types
• fixing inconsistent category labels
• handling missing values
• resolving impossible date relationships

Cleaned datasets are saved in **data/clean/**.

All decisions and assumptions are documented in:

docs/cleaning_report.md

---

## Step 3 — SQL Analysis

The cleaned datasets are loaded into SQLite and analyzed using SQL.

Eight analytical queries answer key business questions such as:

• Total revenue by segment
• Top revenue customers
• Month-over-month revenue change
• Customer churn rate
• Customer support performance
• Cohort retention analysis

All queries are stored in:

sql/queries.sql

Each query includes a short comment describing the business question it answers.

---

## Step 4 — Power BI Dashboard

A three-page Power BI dashboard presents key metrics for leadership.

Pages include:

Executive Summary
Customer Overview
Support Analysis

The dashboard contains KPIs such as:

MRR
ARR
ARPA
Net Revenue Retention
Logo Churn Rate

All pages share interactive filters for:

• Date range
• Customer segment

Dashboard file:

dashboard/dashboard.pbix

---

# Project Structure

```
customer-revenue-support-analysis
│
├── data
│   ├── raw
│   └── clean
│
├── scripts
│   ├── data_generation.py
│   └── cleaning_pipeline.py
│
├── sql
│   └── queries.sql
│
├── docs
│   └── cleaning_report.md
│
├── dashboard
│   └── dashboard.pbix
│
├── requirements.txt
└── README.md
```

---

# Tools & Technologies

Python
Pandas
NumPy
Faker
SQLite
Power BI

---

# Key Metrics Used

MRR — Monthly Recurring Revenue
ARR — Annual Recurring Revenue
ARPA — Average Revenue Per Account
NRR — Net Revenue Retention
CSAT — Customer Satisfaction Score

---

# How to Run the Project

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Generate raw data

```
python scripts/data_generation.py
```

### 3. Clean the datasets

```
python scripts/cleaning_pipeline.py
```

### 4. Run SQL analysis

Load the cleaned data into SQLite and execute:

```
sql/queries.sql
```

### 5. Open the Power BI dashboard

Open:

```
dashboard/dashboard.pbix
```

---

# Purpose of This Project

This project is designed to demonstrate practical data analyst skills including:

data simulation
data quality management
SQL analytics
business metric analysis
dashboard design

The workflow mirrors real-world analytics tasks performed in SaaS companies preparing internal reports and investor presentations.




