import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("market.db")
cursor = conn.cursor()

# Drop all existing tables
tables = ["Company", "Stock", "Financials", "MacroIndicators", "User"]
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Import Companies
print("📥 Importing Companies...")
companies_df = pd.read_csv("Data/companies.csv")
companies_df.to_sql("Company", conn, if_exists="replace", index=False)
print("✔️ Companies imported successfully.")

# Import Stocks
print("📥 Importing Stocks...")
stocks_df = pd.read_csv("Data/stocks.csv")
stocks_df["date"] = pd.to_datetime(stocks_df["date"]).dt.date
stocks_df.to_sql("Stock", conn, if_exists="replace", index=False)
print("✔️ Stocks imported successfully.")

# Import Financials
print("📥 Importing Financials...")
financials_df = pd.read_csv("Data/financials.csv")
financials_df.to_sql("Financials", conn, if_exists="replace", index=False)
print("✔️ Financials imported successfully.")

# 📊 Import Updated Macro Indicators (including External & Banking data)
print("📥 Importing Macro Indicators...")
macro_df = pd.read_csv("Data/macro.csv")  # Updated to use macro.csv
macro_df["date"] = pd.to_datetime(macro_df["date"]).dt.date
macro_df.to_sql("MacroIndicators", conn, if_exists="replace", index=False)
print("✔️ Macro Indicators imported successfully.")

# Optional: Import Users
print("📥 Importing Users...")
try:
    users_df = pd.read_csv("Data/users.csv")
    users_df.to_sql("User", conn, if_exists="replace", index=False)
    print("✔️ Users imported successfully.")
except FileNotFoundError:
    print("⚠️ users.csv not found, skipping User data import.")

# Commit and close connection
conn.commit()
conn.close()
print("✅ All sample data imported successfully.")