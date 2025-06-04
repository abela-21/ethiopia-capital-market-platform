from flask import Blueprint, request, jsonify
from model import db, Financials

financials_api = Blueprint("financials_api", __name__)


@financials_api.route("/financials/<int:company_id>")
def get_financials(company_id):
    year = request.args.get("year", type=int)
    query = Financials.query.filter_by(company_id=company_id)
    if year:
        query = query.filter_by(year=year)
    records = query.all()
    if not records:
        return jsonify({"message": "No financial data found"}), 404
    return jsonify(
        [
            {
                "id": r.id,
                "company_id": r.company_id,
                "year": r.year,
                "revenue": r.revenue,
                "net_profit": r.net_profit,
                "ebitda": r.ebitda,
                "total_assets": r.total_assets,
                "total_liabilities": r.total_liabilities,
                "equity": r.equity,
                "debt_to_equity": r.debt_to_equity,
            }
            for r in records
        ]
    )
