from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ticker = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

class Financials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    net_profit = db.Column(db.Float, nullable=False)
    ebitda = db.Column(db.Float, nullable=False)
    total_assets = db.Column(db.Float, nullable=False)
    total_liabilities = db.Column(db.Float, nullable=False)
    equity = db.Column(db.Float, nullable=False)
    debt_to_equity = db.Column(db.Float, nullable=False)

class MacroIndicators(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    gdp_growth = db.Column(db.Float, nullable=False)
    inflation_rate = db.Column(db.Float, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    etb_usd = db.Column(db.Float, nullable=False)
    etb_eur = db.Column(db.Float, nullable=False)
    etb_gbp = db.Column(db.Float, nullable=False)
    etb_jpy = db.Column(db.Float, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String)