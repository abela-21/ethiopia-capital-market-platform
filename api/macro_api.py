from flask import Blueprint, request, jsonify
from model import db, MacroIndicators
from datetime import datetime

macro_api = Blueprint("macro_api", __name__)


@macro_api.route("/macro_indicators")
def get_macro_indicators():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    query = MacroIndicators.query
    if date_from:
        query = query.filter(
            MacroIndicators.date >= datetime.strptime(date_from, "%Y-%m-%d").date()
        )
    if date_to:
        query = query.filter(
            MacroIndicators.date <= datetime.strptime(date_to, "%Y-%m-%d").date()
        )

    records = query.all()
    return jsonify(
        [
            {
                "id": r.id,
                "date": str(r.date),
                "gdp_growth": r.gdp_growth,
                "inflation_rate": r.inflation_rate,
                "interest_rate": r.interest_rate,
                "etb_usd": r.etb_usd,
                "etb_eur": r.etb_eur,
                "etb_gbp": r.etb_gbp,
                "etb_jpy": r.etb_jpy,
            }
            for r in records
        ]
    )
