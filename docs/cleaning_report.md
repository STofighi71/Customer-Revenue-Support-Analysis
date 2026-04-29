# Data Cleaning Report

## 1. Inconsistent Labels
Enterprise written as "enterprise"
→ Fixed using .str.title()

## 2. Missing Values
CSM missing for SMB customers
→ Filled with "Unassigned"

## 3. Wrong Data Type
amount stored as string
→ Converted using to_numeric()

## 4. Duplicate Rows
Tickets duplicated
→ Removed using drop_duplicates()

## 5. Impossible Dates
close_date < open_date
→ Fixed by setting close_date = open_date + 2 days