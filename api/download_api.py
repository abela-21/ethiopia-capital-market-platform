from flask import Blueprint, send_file, request, jsonify, current_app
from api.models.models import Company, Financial, Stock, MacroIndicators
from api.models import db
from api.utils.errors import APIError
from api.utils.cache import cache
from api.utils.limiter import limiter
from datetime import datetime
import pandas as pd
from io import BytesIO
import logging

# Configure logger
logger = logging.getLogger(__name__)

download_api = Blueprint("download_api", __name__)

def validate_date_range(date_from, date_to):
    """Validate date range parameters"""
    try:
        if date_from:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
        if date_to:
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
            if date_from and date_to < date_from:
                raise ValueError("end_date cannot be earlier than start_date")
        return True
    except ValueError as e:
        raise APIError(str(e), status_code=400)

def create_excel_response(df, filename):
    """Create Excel file response"""
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        # Auto-adjust columns width
        worksheet = writer.sheets['Data']
        for idx, col in enumerate(df.columns):
            max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_length)
    
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@download_api.route("/download/companies")
@limiter.limit("30/minute")
@cache.cached(timeout=300, query_string=True)
def download_companies():
    """Download companies data in CSV or Excel format"""
    try:
        file_format = request.args.get("format", "csv")
        industry = request.args.get("industry")
        sector = request.args.get("sector")

        # Build query
        query = Company.query
        if industry:
            query = query.filter(Company.industry == industry)
        if sector:
            query = query.filter(Company.sector == sector)

        companies = query.all()
        if not companies:
            raise APIError("No companies found", status_code=404)

        # Prepare data
        data = [{
            "ID": c.id,
            "Name": c.name,
            "Ticker": c.ticker,
            "Industry": c.industry,
            "Sector": c.sector,
            "Description": c.description,
            "Website": c.website,
            "Established Date": c.established_date.strftime("%Y-%m-%d") if c.established_date else None
        } for c in companies]

        df = pd.DataFrame(data)
        
        # Return appropriate format
        if file_format.lower() == "excel":
            return create_excel_response(df, "companies.xlsx")
        else:
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name="companies.csv",
                mimetype="text/csv"
            )

    except APIError as e:
        logger.warning(f"API Error in download_companies: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in download_companies: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@download_api.route("/download/financials/<int:company_id>")
@limiter.limit("30/minute")
@cache.cached(timeout=300, query_string=True)
def download_financials(company_id):
    """Download financial data for a specific company"""
    try:
        company = Company.query.get_or_404(company_id)
        year_from = request.args.get("year_from", type=int)
        year_to = request.args.get("year_to", type=int)
        period = request.args.get("period")  # Annual/Q1/Q2/Q3/Q4
        file_format = request.args.get("format", "csv")

        # Build query
        query = Financial.query.filter_by(company_id=company_id)
        if year_from:
            query = query.filter(Financial.year >= year_from)
        if year_to:
            query = query.filter(Financial.year <= year_to)
        if period:
            query = query.filter(Financial.period == period)

        financials = query.all()
        if not financials:
            raise APIError("No financial data found", status_code=404)

        # Prepare data
        data = [{
            "Year": f.year,
            "Period": f.period,
            "Revenue": f.revenue,
            "Cost of Revenue": f.cost_of_revenue,
            "Gross Profit": f.gross_profit,
            "Operating Income": f.operating_income,
            "Net Income": f.net_income,
            "Total Assets": f.total_assets,
            "Total Liabilities": f.total_liabilities,
            "Total Equity": f.total_equity,
            "Current Ratio": f.current_ratio,
            "Debt to Equity": f.debt_to_equity,
            "Return on Equity": f.return_on_equity,
            "Return on Assets": f.return_on_assets,
            "Profit Margin": f.profit_margin
        } for f in financials]

        df = pd.DataFrame(data)
        filename = f"{company.ticker}_financials_{year_from or 'all'}_to_{year_to or 'present'}"

        if file_format.lower() == "excel":
            return create_excel_response(df, f"{filename}.xlsx")
        else:
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f"{filename}.csv",
                mimetype="text/csv"
            )

    except APIError as e:
        logger.warning(f"API Error in download_financials: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in download_financials: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@download_api.route("/download/macro")
@limiter.limit("30/minute")
@cache.cached(timeout=300, query_string=True)
def download_macro():
    """Download macroeconomic indicators with filtering options"""
    try:
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")
        variables = request.args.get("variables")
        file_format = request.args.get("format", "csv")

        # Validate dates if provided
        validate_date_range(date_from, date_to)

        # Build query
        query = MacroIndicators.query
        if date_from:
            query = query.filter(MacroIndicators.date >= date_from)
        if date_to:
            query = query.filter(MacroIndicators.date <= date_to)

        records = query.all()
        if not records:
            raise APIError("No data found for the specified criteria", status_code=404)

        # Convert to DataFrame
        data = [r.__dict__ for r in records]
        df = pd.DataFrame(data)
        df.drop(columns=["_sa_instance_state"], inplace=True)

        # Filter columns if specified
        if variables:
            selected_columns = ["date"] + variables.split(",")
            invalid_cols = [col for col in selected_columns if col not in df.columns]
            if invalid_cols:
                raise APIError(f"Invalid column(s): {', '.join(invalid_cols)}", status_code=400)
            df = df[selected_columns]

        filename = f"macro_indicators_{date_from or 'start'}_to_{date_to or 'present'}"

        if file_format.lower() == "excel":
            return create_excel_response(df, f"{filename}.xlsx")
        else:
            buffer = BytesIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f"{filename}.csv",
                mimetype="text/csv"
            )

    except APIError as e:
        logger.warning(f"API Error in download_macro: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in download_macro: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500