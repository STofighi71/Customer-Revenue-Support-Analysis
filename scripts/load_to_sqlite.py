import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")

customers = pd.read_csv("data/clean/customers_clean.csv")
transactions = pd.read_csv("data/clean/transactions_clean.csv")
tickets = pd.read_csv("data/clean/support_tickets_clean.csv")

customers.to_sql("customers", conn, if_exists="replace", index=False)
transactions.to_sql("transactions", conn, if_exists="replace", index=False)
tickets.to_sql("support_tickets", conn, if_exists="replace", index=False)

conn.close()

print("Data loaded into SQLite database.")