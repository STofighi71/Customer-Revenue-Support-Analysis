
# Data Cleaning Report

This document describes the data quality issues identified in the raw dataset and the steps taken to resolve them during the data cleaning process.

The goal of the cleaning step was to ensure the dataset could be reliably used for SQL analysis in later stages of the project.

---

# 1. Inconsistent Customer Segment Labels

## What was found

The `segment` column in the `customers` dataset contained inconsistent capitalization and formatting. Examples included:

Enterprise
SMB
sMb
MID-MARKET

These inconsistencies can lead to incorrect aggregations when grouping by segment in SQL queries.

## How it was detected

The issue was detected by examining unique values in the `segment` column.

## What was done

All segment values were standardized by converting them to lowercase and mapping them to three valid categories:

enterprise
mid-market
smb

## Assumptions

It was assumed that all variations referred to one of the three intended segments.

---

# 2. Duplicate Customer Records

## What was found

The dataset contained duplicate customer rows intentionally inserted during data generation.

Duplicate rows can cause inflated counts and incorrect revenue totals.

## How it was detected

Duplicates were identified using the `customer_id` column as the unique identifier.

## What was done

Duplicate rows were removed using:

drop_duplicates(subset="customer_id")

This ensured each customer appeared only once in the dataset.

## Assumptions

It was assumed that the first occurrence of each customer record was correct.

---

# 3. Missing MRR Values

## What was found

Some customers had missing values in the `mrr` column. This issue was intentionally introduced for a subset of SMB customers.

Missing MRR values can cause aggregation functions such as SUM() to return NULL results in SQL.

Missing transaction amounts were replaced with 0, assuming no revenue was generated for those records.

## How it was detected

Missing values were detected using null checks on the `mrr` column.

## What was done

Missing MRR values were filled using the median MRR of customers within the same segment.

customers.groupby("segment")["mrr"].transform("median")

## Assumptions

Using the median within each segment provides a reasonable estimate while avoiding distortion from extreme values.

---

# 4. Impossible Transaction Dates

## What was found

Some rows in the `transactions` dataset contained dates far in the future (for example, the year 2099).

These values are unrealistic for a historical revenue dataset.

## How it was detected

Transaction dates were parsed as datetime objects and compared with the current date.

## What was done

Rows containing transaction dates later than the current date were removed.

transactions = transactions[transactions["month"] < pd.Timestamp.today()]

## Assumptions

Future transaction dates were considered data entry errors rather than valid future bookings.

---

# 5. Missing CSAT Scores

## What was found

Some support tickets contained missing values in the `csat_score` column.

## How it was detected

Null values were identified during exploratory inspection of the dataset.

## What was done

Missing CSAT scores were filled with the median CSAT score across the dataset.

tickets["csat_score"].fillna(tickets["csat_score"].median())

## Assumptions

The median CSAT score was used to minimize bias introduced by outliers.

---

# Summary

The following data issues were identified and resolved:

• inconsistent categorical labels
• duplicate records
• missing revenue values
• impossible future dates
• missing satisfaction scores

After cleaning, the datasets were saved to the `data/clean/` directory and used for SQL analysis in Step 3.
