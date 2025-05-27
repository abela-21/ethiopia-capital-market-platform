from flask import Blueprint, jsonify
from model import Company, Stock
from sqlalchemy import func
from model import db

market_api = Blueprint("market_api", __name__)

@market_api.route("/market", methods=["GET"])
def get_market_summary():
    try:
        total_companies = Company.query.count()

        # Assumed number of shares per company for prototype
        assumed_shares_per_company = 10000

        market_cap = 0
        companies = Company.query.all()

        for company in companies:
            latest_stock = (
                Stock.query.filter_by(company_id=company.id)
                .order_by(Stock.date.desc())
                .first()
            )
            if latest_stock:
                market_cap += latest_stock.close * assumed_shares_per_company

        latest_date = db.session.query(func.max(Stock.date)).scalar()
        latest_date_str = latest_date.strftime("%Y-%m-%d") if latest_date else "N/A"

        summary = {
            "total_companies": total_companies,
            "market_cap": market_cap,
            "last_updated": latest_date_str,
        }

        return jsonify(summary), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
