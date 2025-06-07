from flask import Blueprint, request, jsonify, current_app
from api.models.models import MacroIndicators
from api.models import db
from api.utils.cache import cache
from api.utils.limiter import limiter
from api.utils.errors import APIError
from datetime import datetime, timedelta
from sqlalchemy import desc, asc
import logging

# Configure logger
logger = logging.getLogger(__name__)

macro_api = Blueprint("macro_api", __name__)

def validate_date_range(date_from, date_to):
    """Validate date range parameters"""
    try:
        if date_from:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        if date_to:
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
            if date_from and date_to < date_from:
                raise ValueError("end_date cannot be earlier than start_date")
        return True
    except ValueError as e:
        raise APIError(str(e), status_code=400)

def serialize_macro(record):
    """Helper function to serialize macro indicators"""
    return {
        "id": record.id,
        "date": record.date.strftime("%Y-%m-%d"),
        # Real Sector
        "gdp_growth": float(record.gdp_growth) if record.gdp_growth else None,
        "gdp_per_capita": float(record.gdp_per_capita) if record.gdp_per_capita else None,
        "inflation_rate": float(record.inflation_rate) if record.inflation_rate else None,
        "interest_rate": float(record.interest_rate) if record.interest_rate else None,
        "unemployment_rate": float(record.unemployment_rate) if record.unemployment_rate else None,
        # Foreign Exchange
        "etb_usd": float(record.etb_usd) if record.etb_usd else None,
        "etb_eur": float(record.etb_eur) if record.etb_eur else None,
        "etb_gbp": float(record.etb_gbp) if record.etb_gbp else None,
        "etb_jpy": float(record.etb_jpy) if record.etb_jpy else None,
        # Banking Sector
        "total_deposits": float(record.total_deposits) if record.total_deposits else None,
        "total_loans": float(record.total_loans) if record.total_loans else None,
        "npl_ratio": float(record.npl_ratio) if record.npl_ratio else None
    }

@macro_api.route("/macro/indicators")
@cache.cached(timeout=300, query_string=True)
@limiter.limit("30/minute")
def get_macro_indicators():
    """Get macro indicators with optional date range and filters"""
    try:
        # Get query parameters
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")
        sort = request.args.get("sort", "desc")
        limit = request.args.get("limit", type=int)
        
        # Validate date range
        validate_date_range(date_from, date_to)
        
        # Build query
        query = MacroIndicators.query
        
        if date_from:
            query = query.filter(MacroIndicators.date >= datetime.strptime(date_from, "%Y-%m-%d"))
        if date_to:
            query = query.filter(MacroIndicators.date <= datetime.strptime(date_to, "%Y-%m-%d"))
            
        # Apply sorting
        sort_func = desc if sort == "desc" else asc
        query = query.order_by(sort_func(MacroIndicators.date))
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        records = query.all()
        if not records:
            raise APIError("No data found for the specified criteria", status_code=404)
        
        response = {
            "data": [serialize_macro(r) for r in records],
            "metadata": {
                "count": len(records),
                "date_from": date_from,
                "date_to": date_to,
                "sort": sort
            }
        }
        
        return jsonify(response), 200
        
    except APIError as e:
        logger.warning(f"API Error in get_macro_indicators: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_macro_indicators: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@macro_api.route("/macro/latest")
@cache.cached(timeout=60)
@limiter.limit("60/minute")
def get_latest_indicators():
    """Get latest macro indicators"""
    try:
        latest = MacroIndicators.query.order_by(desc(MacroIndicators.date)).first()
        
        if not latest:
            raise APIError("No macro data found", status_code=404)
        
        response = {
            "latest_indicators": serialize_macro(latest),
            "as_of": latest.date.strftime("%Y-%m-%d")
        }
        
        return jsonify(response), 200
        
    except APIError as e:
        logger.warning(f"API Error in get_latest_indicators: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_latest_indicators: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@macro_api.route("/macro/summary")
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_macro_summary():
    """Get macro indicators summary with trends"""
    try:
        # Get latest record
        latest = MacroIndicators.query.order_by(desc(MacroIndicators.date)).first()
        if not latest:
            raise APIError("No macro data found", status_code=404)
            
        # Get record from previous month
        prev_month = latest.date - timedelta(days=30)
        previous = MacroIndicators.query.filter(
            MacroIndicators.date <= prev_month
        ).order_by(desc(MacroIndicators.date)).first()
        
        # Calculate changes
        changes = {}
        if previous:
            changes = {
                "inflation_change": latest.inflation_rate - previous.inflation_rate if all([latest.inflation_rate, previous.inflation_rate]) else None,
                "interest_rate_change": latest.interest_rate - previous.interest_rate if all([latest.interest_rate, previous.interest_rate]) else None,
                "fx_usd_change": ((latest.etb_usd - previous.etb_usd) / previous.etb_usd * 100) if all([latest.etb_usd, previous.etb_usd]) else None
            }
        
        response = {
            "current": serialize_macro(latest),
            "monthly_changes": changes,
            "as_of": latest.date.strftime("%Y-%m-%d")
        }
        
        return jsonify(response), 200
        
    except APIError as e:
        logger.warning(f"API Error in get_macro_summary: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_macro_summary: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500