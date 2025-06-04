from flask import Blueprint, send_file, request, jsonify
from model import db, Company, Financials, MacroIndicators
import pandas as pd
from io import BytesIO

download_api = Blueprint("download_api", __name__)

# 📥 Download Companies Data
@download_api.route("/download/companies")
def download_companies():
    companies = Company.query.all()
    data = [{
        "ID": c.id,
        "Name": c.name,
        "Ticker": c.ticker,
        "Industry": c.industry,
        "Description": c.description
    } for c in companies]

    df = pd.DataFrame(data)
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="companies.csv", mimetype="text/csv")


# 📥 Download Financials Data (with optional year filter and format)
@download_api.route("/download/financials/<int:company_id>")
def download_financials(company_id):
    year_from = request.args.get("year_from", type=int)
    year_to = request.args.get("year_to", type=int)
    file_format = request.args.get("format", "csv")

    query = Financials.query.filter_by(company_id=company_id)
    if year_from:
        query = query.filter(Financials.year >= year_from)
    if year_to:
        query = query.filter(Financials.year <= year_to)

    financials = query.all()
    if not financials:
        return {"message": "No financial data found"}, 404

    data = [{
        "Year": f.year,
        "Revenue": f.revenue,
        "Net Profit": f.net_profit,
        "EBITDA": f.ebitda,
        "Total Assets": f.total_assets,
        "Total Liabilities": f.total_liabilities,
        "Equity": f.equity,
        "Debt to Equity": f.debt_to_equity
    } for f in financials]

    df = pd.DataFrame(data)
    buffer = BytesIO()

    if file_format == "excel":
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"financials_company_{company_id}.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"financials_company_{company_id}.csv", mimetype="text/csv")


# 📥 Enhanced Download MacroIndicators (with date, variable filters and format)
@download_api.route("/download/macro_indicators")
def download_macro():
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    variables = request.args.get("variables")  # comma-separated e.g. "gdp_growth,inflation_rate"
    file_format = request.args.get("format", "csv")

    query = MacroIndicators.query
    if date_from:
        query = query.filter(MacroIndicators.date >= date_from)
    if date_to:
        query = query.filter(MacroIndicators.date <= date_to)

    records = query.all()
    if not records:
        return jsonify({"message": "No data for selected filters"}), 404

    # Convert to DataFrame
    data = [r.__dict__ for r in records]
    df = pd.DataFrame(data)
    df.drop(columns=["_sa_instance_state"], inplace=True)

    # Apply variable selection if provided
    if variables:
        selected_columns = ["date"] + variables.split(",")
        # Validate if requested columns exist in df
        missing_cols = [col for col in selected_columns if col not in df.columns]
        if missing_cols:
            return jsonify({"message": f"Invalid column(s): {', '.join(missing_cols)}"}), 400
        df = df[selected_columns]

    # Export as Excel or CSV
    buffer = BytesIO()

    if file_format == "excel":
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name="macro_indicators.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name="macro_indicators.csv",
            mimetype="text/csv"
        )
