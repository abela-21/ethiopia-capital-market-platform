from flask import Blueprint, jsonify, request
from model import Stock, Company
from datetime import datetime

stock_api = Blueprint("stock_api", __name__)

@stock_api.route("/stocks/<int:company_id>", methods=["GET"])
def get_stocks(company_id):
    try:
        # Check if company exists
        company = Company.query.get(company_id)
        if not company:
            return jsonify({"error": f"Company ID {company_id} not found"}), 404

        # Get optional date filters
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        query = Stock.query.filter_by(company_id=company_id)

        # Apply date filters if present
        if start_date:
            query = query.filter(Stock.date >= datetime.strptime(start_date, "%Y-%m-%d"))
        if end_date:
            query = query.filter(Stock.date <= datetime.strptime(end_date, "%Y-%m-%d"))

        stocks = query.order_by(Stock.date.asc()).all()

        stock_data = [
            {
                "date": stock.date.strftime("%Y-%m-%d"),
                "open": stock.open,
                "close": stock.close,
                "high": stock.high,
                "low": stock.low,
                "volume": stock.volume,
            }
            for stock in stocks
        ]

        return jsonify(stock_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
