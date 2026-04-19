# Data Cleaning Report
Customer Revenue & Support Analysis

This document describes the data quality issues identified in the raw datasets and the steps taken to resolve them.

The raw datasets were generated intentionally with several issues to simulate common real-world data problems. The cleaning process was implemented in the script `cleaning_pipeline.py`.

---

# Issue 1 — Duplicate Rows in Transactions

### What was found

The transactions dataset contained an exact duplicate row.  
This issue was intentionally introduced during the data generation process to simulate duplicate records caused by data ingestion errors.

### How it was detected

Duplicate rows were identified using the pandas method:

df.duplicated()

The dataset originally contained 501 rows, although only 500 unique transactions were expected.

### How it was fixed

Duplicate rows were removed using:

df.drop_duplicates()

### Assumptions

Exact duplicates represent unintended replication of the same record and should not be counted twice in financial calculations.

### Alternative approaches

Another possible approach would be to deduplicate based on a subset of columns (for example `transaction_id`).  
However, since the duplicate row was identical across all columns, removing full duplicates was the safest approach.

---

# Issue 2 — Incorrect Data Type in Transaction Amount

### What was found

One value in the `amount` column was stored as a string instead of a numeric value.

Since the column represents revenue amounts, it should contain numeric values only.

### How it was detected

The column data type was inspected and one entry was found to be a string value (`"1500"`).

### How it was fixed

The entire column was converted to numeric using:

pd.to_numeric(df["amount"], errors="coerce")

### Assumptions

Transaction amounts must always be numeric.  
If non-numeric values are encountered, they are converted to `NaN` to prevent calculation errors.

### Alternative approaches

Instead of coercing invalid values to `NaN`, the rows could also be removed or manually corrected.  
In this case coercion was chosen because it safely preserves the rest of the dataset.

---

# Issue 3 — Impossible Date Relationship in Support Tickets

### What was found

A support ticket had a `close_date` that occurred before its `open_date`.

This represents an impossible chronological sequence.

### How it was detected

Rows where:

close_date < open_date

were identified as invalid.

### How it was fixed

For those rows, the `close_date` was adjusted to match the `open_date`.

### Assumptions

The most likely explanation is that the ticket was resolved on the same day it was opened.

### Alternative approaches

Another approach could have been to remove the row entirely or flag it for manual review.  
However, since only a small number of rows were affected, correcting the date was considered acceptable.

---

# Issue 4 — Inconsistent Category Labels in Customer Segment

### What was found

The `segment` column contained inconsistent capitalization:

Enterprise  
enterprise  
ENTERPRISE  

Although they represent the same category.

### How it was detected

Unique values in the column were inspected and multiple capitalization variants were identified.

### How it was fixed

The labels were standardized using:

df["segment"] = df["segment"].str.lower().str.title()

### Assumptions

All capitalization variants refer to the same business segment.

### Alternative approaches

Another approach would be mapping categories using a dictionary (for example via `replace()`).

The chosen approach was simpler and scalable for similar inconsistencies.

---

# Issue 5 — Pattern-Based Missing Values in MRR

### What was found

All customers belonging to the SMB segment had missing values in the `mrr` column.

The missing values were not random but followed a clear pattern based on customer segment.

### How it was detected

A group-by inspection of missing values revealed that only SMB customers were affected.

### How it was fixed

Missing MRR values for SMB customers were replaced with the median MRR of the SMB segment.

### Assumptions

The median was chosen because it is less sensitive to extreme values than the mean.

### Alternative approaches

Possible alternatives include:

• Filling with the mean  
• Filling with a constant value  
• Leaving the values missing

The median was selected because it provides a robust estimate without introducing large bias.

---

# Summary

Five data quality issues were detected and resolved:

1. Duplicate transaction rows removed  
2. Incorrect numeric data types corrected  
3. Impossible date relationships fixed  
4. Inconsistent categorical labels standardized  
5. Pattern-based missing values imputed using median values

The cleaned datasets were saved to:

data/clean/

These cleaned datasets are used in the next step of the project for SQL-based analysis.