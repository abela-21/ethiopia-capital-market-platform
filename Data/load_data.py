import pandas as pd
from datetime import datetime
import sys

# Add your project path so imports work
sys.path.append("/users/abela/Downloads/Project X")

from model import db, MacroIndicators, Company, User
from app import app
from sqlalchemy.sql import text

def load_companies():
    print("📥 Loading companies...")
    df = pd.read_csv("/users/abela/Downloads/Project X/Data/companies.csv")
    with app.app_context():
        for _, row in df.iterrows():
            record = Company(
                id=row["id"],
                name=row["name"],
                ticker=row["ticker"],
                industry=row["industry"],
                description=row["description"]
            )
            db.session.add(record)
        db.session.commit()
    print("✔️ Companies loaded successfully.")

def load_financials():
    print("📥 Loading financials...")
    df = pd.read_csv("/users/abela/Downloads/Project X/Data/financials.csv")
    with app.app_context():
        for _, row in df.iterrows():
            db.session.execute(
                text("INSERT INTO Financials (id, company_id, year, revenue, ebitda, net_profit, debt_to_equity) VALUES (:id, :company_id, :year, :revenue, :ebitda, :net_profit, :debt_to_equity)"),
                {
                    "id": row["id"],
                    "company_id": row["company_id"],
                    "year": row["year"],
                    "revenue": row["revenue"],
                    "ebitda": row["ebitda"],
                    "net_profit": row["net_profit"],
                    "debt_to_equity": row["debt_to_equity"]
                }
            )
        db.session.commit()
    print("✔️ Financials loaded successfully.")

def load_macro_indicators():
    print("📥 Loading macro indicators...")
    df = pd.read_csv("/users/abela/Downloads/Project X/Data/macro.csv")
    with app.app_context():
        for _, row in df.iterrows():
            record = MacroIndicators(
                date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
                gdp_growth=row["gdp_growth"],
                inflation_rate=row["inflation_rate"],
                interest_rate=row["interest_rate"],
                etb_usd=row["etb_usd"],
                etb_eur=row["etb_eur"],
                etb_gbp=row["etb_gbp"],
                etb_jpy=row["etb_jpy"],
                fx_reserves=row.get("fx_reserves"),
                trade_balance=row.get("trade_balance"),
                current_account_balance=row.get("current_account_balance"),
                total_loans=row.get("total_loans"),
                total_deposits=row.get("total_deposits"),
                npl_ratio=row.get("npl_ratio")
            )
            db.session.add(record)
        db.session.commit()
    print("✔️ Macro indicators loaded successfully.")

def load_users():
    print("📥 Loading users...")
    try:
        df = pd.read_csv("/users/abela/Downloads/Project X/Data/users.csv")
        with app.app_context():
            for _, row in df.iterrows():
                record = User(
                    id=row["id"],
                    username=row["username"],
                    password=row["password"],
                    email=row["email"]
                )
                db.session.add(record)
            db.session.commit()
        print("✔️ Users loaded successfully.")
    except FileNotFoundError:
        print("⚠️ users.csv not found, skipping User data import.")

if __name__ == "__main__":
    print("🚀 Starting data import...")
    load_companies()
    load_financials()
    load_macro_indicators()
    load_users()
    print("✅ All data loaded successfully.")