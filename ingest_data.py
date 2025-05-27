import pandas as pd
import sqlite3

conn = sqlite3.connect("market.db")
cursor = conn.cursor()

companies_df = pd.read_csv("companies.csv")
companies_df.to_sql("Company", conn, if_exists="replace", index=False)

stocks_df = pd.read_csv("stocks.csv")
stocks_df["date"] = pd.to_datetime(stocks_df["date"]).dt.date
stocks_df.to_sql("Stock", conn, if_exists="replace", index=False)

financials_df = pd.read_csv("financials.csv")
financials_df.to_sql("Financials", conn, if_exists="replace", index=False)

macro_df = pd.read_csv("macro_indicators.csv")
macro_df["date"] = pd.to_datetime(macro_df["date"]).dt.date
macro_df.to_sql("MacroIndicators", conn, if_exists="replace", index=False)

try:
    users_df = pd.read_csv("users.csv")
    users_df.to_sql("User", conn, if_exists="replace", index=False)
except FileNotFoundError:
    print("users.csv not found, skipping User data import.")

conn.commit()
conn.close()
print("Sample data imported successfully.")
