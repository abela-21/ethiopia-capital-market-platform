from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ticker = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)


class Financials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    net_profit = db.Column(db.Float, nullable=False)
    ebitda = db.Column(db.Float, nullable=False)
    total_assets = db.Column(db.Float, nullable=False)
    total_liabilities = db.Column(db.Float, nullable=False)
    equity = db.Column(db.Float, nullable=False)
    debt_to_equity = db.Column(db.Float, nullable=False)


class MacroIndicators(db.Model):
    __tablename__ = "MacroIndicators"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    gdp_growth = db.Column(db.Float, nullable=False)
    inflation_rate = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    etb_usd = db.Column(db.Float, nullable=False)
    etb_eur = db.Column(db.Float, nullable=False)
    etb_gbp = db.Column(db.Float, nullable=False)
    etb_jpy = db.Column(db.Float, nullable=False)
    
    # 📊 New External Sector fields:
    fx_reserves = db.Column(db.Float, nullable=True)
    trade_balance = db.Column(db.Float, nullable=True)
    current_account_balance = db.Column(db.Float, nullable=True)
    
    # 📊 New Banking Sector fields:
    total_loans = db.Column(db.Float, nullable=True)
    total_deposits = db.Column(db.Float, nullable=True)
    npl_ratio = db.Column(db.Float, nullable=True)



bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    
    
