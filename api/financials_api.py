from flask import Blueprint, request, jsonify, current_app
from api.models.models import Financial, Company
from api.models import db
from api.utils.cache import cache
from api.utils.limiter import limiter
from api.utils.errors import APIError
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import desc, asc
import logging

# Configure logger
logger = logging.getLogger(__name__)

financials_api = Blueprint("financials_api", __name__)

def serialize_financial(record):
    """Helper function to serialize financial data"""
    return {
        "id": record.id,
        "company_id": record.company_id,
        "year": record.year,
        "period": record.period,
        # Income Statement
        "revenue": float(record.revenue) if record.revenue else None,
        "cost_of_revenue": float(record.cost_of_revenue) if record.cost_of_revenue else None,
        "gross_profit": float(record.gross_profit) if record.gross_profit else None,
        "operating_expenses": float(record.operating_expenses) if record.operating_expenses else None,
        "operating_income": float(record.operating_income) if record.operating_income else None,
        "net_income": float(record.net_income) if record.net_income else None,
        # Balance Sheet
        "total_assets": float(record.total_assets) if record.total_assets else None,
        "total_liabilities": float(record.total_liabilities) if record.total_liabilities else None,
        "total_equity": float(record.total_equity) if record.total_equity else None,
        # Ratios
        "current_ratio": float(record.current_ratio) if record.current_ratio else None,
        "debt_to_equity": float(record.debt_to_equity) if record.debt_to_equity else None,
        "return_on_equity": float(record.return_on_equity) if record.return_on_equity else None,
        "return_on_assets": float(record.return_on_assets) if record.return_on_assets else None,
        "profit_margin": float(record.profit_margin) if record.profit_margin else None,
        # Metadata
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None
    }

@financials_api.route("/financials/<int:company_id>")
@cache.cached(timeout=300, query_string=True)
@limiter.limit("30/minute")
def get_financials(company_id):
    """Get financial records for a company with optional filters"""
    try:
        # Check if company exists
        company = Company.query.get_or_404(company_id)
        
        # Get query parameters
        year = request.args.get("year", type=int)
        period = request.args.get("period")  # Annual/Q1/Q2/Q3/Q4
        sort = request.args.get("sort", "desc")
        limit = request.args.get("limit", type=int)
        
        # Build query
        query = Financial.query.filter_by(company_id=company_id)
        
        if year:
            query = query.filter_by(year=year)
        if period:
            query = query.filter_by(period=period)
            
        # Apply sorting
        sort_func = desc if sort == "desc" else asc
        query = query.order_by(sort_func(Financial.year), sort_func(Financial.period))
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        records = query.all()
        if not records:
            raise APIError("No financial data found", status_code=404)
        
        response = {
            "company": {
                "id": company.id,
                "name": company.name,
                "ticker": company.ticker
            },
            "data": [serialize_financial(r) for r in records],
            "metadata": {
                "count": len(records),
                "year": year,
                "period": period,
                "sort": sort
            }
        }
        
        return jsonify(response), 200
        
    except APIError as e:
        logger.warning(f"API Error in get_financials: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_financials: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@financials_api.route("/financials/<int:company_id>/latest")
@cache.cached(timeout=60)
@limiter.limit("60/minute")
def get_latest_financials(company_id):
    """Get latest financial record for a company"""
    try:
        company = Company.query.get_or_404(company_id)
        
        latest = Financial.query.filter_by(company_id=company_id)\
            .order_by(desc(Financial.year), desc(Financial.period))\
            .first()
            
        if not latest:
            raise APIError("No financial data found", status_code=404)
        
        response = {
            "company": {
                "id": company.id,
                "name": company.name,
                "ticker": company.ticker
            },
            "latest_financials": serialize_financial(latest)
        }
        
        return jsonify(response), 200
        
    except APIError as e:
        logger.warning(f"API Error in get_latest_financials: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_latest_financials: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@financials_api.route("/financials/<int:company_id>/summary")
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_financials_summary(company_id):
    """Get financial summary for a company"""
    try:
        company = Company.query.get_or_404(company_id)
        
        # Get latest annual financials
        latest = Financial.query.filter_by(
            company_id=company_id,
            period='Annual'
        ).order_by(desc(Financial.year)).first()
        
        if not latest:
            raise APIError("No financial data found", status_code=404)
            
        # Calculate year-over-year growth
        previous = Financial.query.filter_by(
            company_id=company_id,
            period='Annual',
            year=latest.year - 1
        ).first()
        
        growth = {}
        if previous:
            growth = {
                "revenue_growth": ((latest.revenue - previous.revenue) / previous.revenue * 100) 
                    if previous.revenue else None,
                "profit_growth": ((latest.net_income - previous.net_income) / previous.net_income * 100) 
                    if previous.net_income else None,
                "assets_growth": ((latest.total_assets - previous.total_assets) / previous.total_assets * 100) 
                    if previous.total_assets else None
            }
        
        response = {
            "company": {
                "id": company.id,
                "name": company.name,
                "ticker": company.ticker
            },
            "latest_annual": serialize_financial(latest),
            "year_over_year_growth": growth
        }
        
        return jsonify(response), 200
        
    except APIError as e:
        logger.warning(f"API Error in get_financials_summary: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_financials_summary: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500