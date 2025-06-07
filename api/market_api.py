from flask import Blueprint, jsonify, request, current_app
from api.models.models import Company, Stock
from api.models import db
from api.utils.cache import cache
from api.utils.limiter import limiter
from api.utils.errors import APIError
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import logging

# Configure logger
logger = logging.getLogger(__name__)

market_api = Blueprint("market_api", __name__)

def calculate_market_metrics(companies, date=None):
    """Calculate key market metrics"""
    total_market_cap = 0
    active_companies = 0
    total_volume = 0
    gainers = 0
    losers = 0

    for company in companies:
        query = Stock.query.filter_by(company_id=company.id)
        if date:
            query = query.filter(Stock.date <= date)
        
        latest_stock = query.order_by(desc(Stock.date)).first()
        if latest_stock:
            market_cap = latest_stock.close * company.shares_outstanding
            total_market_cap += market_cap
            total_volume += latest_stock.volume
            active_companies += 1
            
            prev_stock = Stock.query.filter_by(company_id=company.id)\
                .filter(Stock.date < latest_stock.date)\
                .order_by(desc(Stock.date)).first()
            
            if prev_stock:
                if latest_stock.close > prev_stock.close:
                    gainers += 1
                elif latest_stock.close < prev_stock.close:
                    losers += 1

    return {
        "total_market_cap": round(total_market_cap, 2),
        "active_companies": active_companies,
        "total_volume": total_volume,
        "gainers": gainers,
        "losers": losers
    }

@market_api.route("/market/summary")
@cache.cached(timeout=300)
@limiter.limit("60/minute")
def get_market_summary():
    """Get market summary with key metrics"""
    try:
        companies = Company.query.all()
        if not companies:
            raise APIError("No companies found in the market", status_code=404)

        latest_date = db.session.query(func.max(Stock.date)).scalar()
        if not latest_date:
            raise APIError("No trading data available", status_code=404)

        metrics = calculate_market_metrics(companies, latest_date)

        response = {
            "summary": {
                "total_companies": len(companies),
                "active_companies": metrics["active_companies"],
                "market_cap": metrics["total_market_cap"],
                "daily_volume": metrics["total_volume"],
                "gainers": metrics["gainers"],
                "losers": metrics["losers"],
                "unchanged": metrics["active_companies"] - metrics["gainers"] - metrics["losers"]
            },
            "metadata": {
                "last_updated": latest_date.strftime("%Y-%m-%d"),
                "currency": "ETB"
            }
        }

        return jsonify(response), 200

    except APIError as e:
        logger.warning(f"API Error in get_market_summary: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_market_summary: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@market_api.route("/market/trends")
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_market_trends():
    """Get market trends over time"""
    try:
        days = request.args.get("days", default=30, type=int)
        if days <= 0:
            raise APIError("Days parameter must be positive", status_code=400)

        latest_date = db.session.query(func.max(Stock.date)).scalar()
        if not latest_date:
            raise APIError("No trading data available", status_code=404)

        start_date = latest_date - timedelta(days=days)
        companies = Company.query.all()

        daily_metrics = []
        current_date = start_date
        while current_date <= latest_date:
            metrics = calculate_market_metrics(companies, current_date)
            if metrics["active_companies"] > 0:
                daily_metrics.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "market_cap": metrics["total_market_cap"],
                    "volume": metrics["total_volume"],
                    "gainers": metrics["gainers"],
                    "losers": metrics["losers"]
                })
            current_date += timedelta(days=1)

        response = {
            "trends": daily_metrics,
            "metadata": {
                "period": f"Last {days} days",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": latest_date.strftime("%Y-%m-%d")
            }
        }

        return jsonify(response), 200

    except APIError as e:
        logger.warning(f"API Error in get_market_trends: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_market_trends: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@market_api.route("/market/leaders")
@cache.cached(timeout=300)
@limiter.limit("30/minute")
def get_market_leaders():
    """Get market leaders and laggards"""
    try:
        latest_date = db.session.query(func.max(Stock.date)).scalar()
        if not latest_date:
            raise APIError("No trading data available", status_code=404)

        prev_date = db.session.query(Stock.date)\
            .filter(Stock.date < latest_date)\
            .order_by(desc(Stock.date)).first()
        if not prev_date:
            raise APIError("Insufficient data for comparison", status_code=404)

        companies = Company.query.all()
        performance = []

        for company in companies:
            latest = Stock.query.filter_by(
                company_id=company.id,
                date=latest_date
            ).first()
            
            previous = Stock.query.filter_by(
                company_id=company.id,
                date=prev_date[0]
            ).first()

            if latest and previous:
                change = ((latest.close - previous.close) / previous.close) * 100
                performance.append({
                    "company_id": company.id,
                    "ticker": company.ticker,
                    "name": company.name,
                    "price": round(latest.close, 2),
                    "change": round(change, 2),
                    "volume": latest.volume
                })

        gainers = sorted(performance, key=lambda x: x["change"], reverse=True)[:5]
        losers = sorted(performance, key=lambda x: x["change"])[:5]

        response = {
            "market_leaders": {
                "top_gainers": gainers,
                "top_losers": losers
            },
            "metadata": {
                "date": latest_date.strftime("%Y-%m-%d"),
                "previous_date": prev_date[0].strftime("%Y-%m-%d")
            }
        }

        return jsonify(response), 200

    except APIError as e:
        logger.warning(f"API Error in get_market_leaders: {str(e)}")
        return jsonify({"error": str(e)}), e.status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_market_leaders: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500