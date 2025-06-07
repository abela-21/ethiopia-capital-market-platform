from flask import Blueprint, jsonify, request, current_app
from api.models.models import Company, CompanyAudit  # Updated import path
from api.models import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.errors import APIError
from api.utils.validators import validate_company_data
from api.utils.cache import cache
from api.utils.limiter import limiter
from datetime import datetime
from sqlalchemy import desc, asc, or_
import logging
from urllib.parse import urlparse
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

company_api = Blueprint('company_api', __name__)

@company_api.before_request
def before_request():
    """Enhanced request logging"""
    if not request.path.endswith('/health'):
        logging.info({
            'path': request.path,
            'method': request.method,
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'params': dict(request.args),
            'user_id': get_jwt_identity() if request.endpoint != 'login' else None
        })

def serialize_company(company):
    """Helper function to serialize company data"""
    return {
        'id': company.id,
        'name': company.name,
        'ticker': company.ticker,
        'industry': company.industry,
        'sector': company.sector,
        'description': company.description,
        'website': company.website,
        'established_date': company.established_date.isoformat() if company.established_date else None,
        'created_at': company.created_at.isoformat() if company.created_at else None,
        'updated_at': company.updated_at.isoformat() if company.updated_at else None,
        'created_by': company.created_by,
        'updated_by': company.updated_by
    }

def add_audit_log(company_id, action, user_id, details=None):
    """Add audit log entry"""
    audit = CompanyAudit(
        company_id=company_id,
        action=action,
        user_id=user_id,
        details=details,
        timestamp=datetime.utcnow()
    )
    db.session.add(audit)

@company_api.route('/companies', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
@limiter.limit("30/minute")
def get_companies():
    """
    Get companies with filtering, sorting and pagination
    ---
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
      - name: industry
        in: query
        type: string
      - name: sector
        in: query
        type: string
      - name: sort_by
        in: query
        type: string
        default: name
      - name: order
        in: query
        type: string
        default: asc
      - name: search
        in: query
        type: string
    responses:
      200:
        description: List of companies
      400:
        description: Bad request
    """
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtering parameters
        industry = request.args.get('industry')
        sector = request.args.get('sector')
        
        # Sorting parameters
        sort_by = request.args.get('sort_by', 'name')
        order = request.args.get('order', 'asc')
        
        # Build query
        query = Company.query
        
        # Apply filters
        if industry:
            query = query.filter(Company.industry == industry)
        if sector:
            query = query.filter(Company.sector == sector)
            
        # Apply search
        search = request.args.get('search')
        if search:
            search_term = f"%{search}%"
            query = query.filter(or_(
                Company.name.ilike(search_term),
                Company.ticker.ilike(search_term),
                Company.industry.ilike(search_term),
                Company.description.ilike(search_term)
            ))
            
        # Apply sorting
        sort_column = getattr(Company, sort_by, Company.name)
        if order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
            
        # Execute paginated query
        paginated = query.paginate(page=page, per_page=per_page)
        
        # Prepare response
        response = {
            'companies': [serialize_company(c) for c in paginated.items],
            'pagination': {
                'total_items': paginated.total,
                'total_pages': paginated.pages,
                'current_page': page,
                'per_page': per_page
            },
            'filters': {
                'industry': industry,
                'sector': sector,
                'search': search
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logging.error(f"Error in get_companies: {str(e)}")
        raise APIError(str(e))

@company_api.route('/companies/<int:id>', methods=['GET'])
@cache.memoize(300)
def get_company_by_id(id):
    """Get single company by ID"""
    try:
        company = Company.query.get_or_404(id)
        return jsonify(serialize_company(company)), 200
    except Exception as e:
        raise APIError(str(e))

@company_api.route('/companies', methods=['POST'])
@jwt_required()
@limiter.limit("5/minute")
def create_company():
    """Create new company"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Validate input data
        errors = validate_company_data(data)
        if errors:
            raise APIError("; ".join(errors))
        
        # Check for duplicate ticker
        if Company.query.filter_by(ticker=data['ticker']).first():
            raise APIError("Company with this ticker already exists", status_code=409)
        
        # Parse established_date if provided
        established_date = None
        if 'established_date' in data:
            try:
                established_date = datetime.strptime(data['established_date'], '%Y-%m-%d').date()
            except ValueError:
                raise APIError("Invalid established_date format. Use YYYY-MM-DD")
        
        # Create company
        new_company = Company(
            name=data['name'],
            ticker=data['ticker'],
            industry=data['industry'],
            sector=data.get('sector'),
            description=data.get('description'),
            website=data.get('website'),
            established_date=established_date,
            created_by=user_id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_company)
        db.session.flush()  # Get ID before commit
        
        # Add audit log
        add_audit_log(new_company.id, 'CREATE', user_id, data)
        
        db.session.commit()
        cache.delete_memoized(get_companies)
        
        return jsonify(serialize_company(new_company)), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in create_company: {str(e)}")
        raise APIError(str(e))

@company_api.route('/companies/<int:id>', methods=['PUT'])
@jwt_required()
def update_company(id):
    """Update existing company"""
    try:
        company = Company.query.get_or_404(id)
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Store original state for audit
        original_state = serialize_company(company)
        
        # Update fields if provided
        for field in ['name', 'industry', 'sector', 'description', 'website']:
            if field in data:
                setattr(company, field, data[field])
        
        if 'established_date' in data:
            try:
                company.established_date = datetime.strptime(data['established_date'], '%Y-%m-%d').date()
            except ValueError:
                raise APIError("Invalid established_date format. Use YYYY-MM-DD")
        
        company.updated_by = user_id
        company.updated_at = datetime.utcnow()
        
        # Add audit log
        add_audit_log(
            company.id, 
            'UPDATE', 
            user_id, 
            {'before': original_state, 'after': data}
        )
        
        db.session.commit()
        cache.delete_memoized(get_company_by_id, id)
        cache.delete_memoized(get_companies)
        
        return jsonify(serialize_company(company)), 200

    except Exception as e:
        db.session.rollback()
        raise APIError(str(e))

@company_api.route('/companies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_company(id):
    """Delete company"""
    try:
        company = Company.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Add audit log before deletion
        add_audit_log(
            company.id, 
            'DELETE', 
            user_id, 
            serialize_company(company)
        )
        
        db.session.delete(company)
        db.session.commit()
        
        cache.delete_memoized(get_company_by_id, id)
        cache.delete_memoized(get_companies)
        
        return jsonify({'message': f'Company {id} deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        raise APIError(str(e))

@company_api.route('/companies/industries', methods=['GET'])
@cache.cached(timeout=3600)
def get_industries():
    """Get list of unique industries"""
    try:
        industries = db.session.query(Company.industry).distinct().all()
        return jsonify([i[0] for i in industries if i[0]]), 200
    except Exception as e:
        raise APIError(str(e))

@company_api.route('/companies/sectors', methods=['GET'])
@cache.cached(timeout=3600)
def get_sectors():
    """Get list of unique sectors"""
    try:
        sectors = db.session.query(Company.sector).distinct().all()
        return jsonify([s[0] for s in sectors if s[0]]), 200
    except Exception as e:
        raise APIError(str(e))

@company_api.route('/companies/batch', methods=['POST'])
@jwt_required()
@limiter.limit("2/minute")
def batch_create_companies():
    """Batch create companies"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not isinstance(data, list):
            raise APIError("Expected array of companies")
        
        companies = []
        for item in data:
            errors = validate_company_data(item)
            if errors:
                raise APIError(f"Invalid company data: {'; '.join(errors)}")
            
            company = Company(
                **item,
                created_by=user_id,
                created_at=datetime.utcnow()
            )
            companies.append(company)
        
        db.session.bulk_save_objects(companies)
        db.session.commit()
        
        # Add audit logs for batch creation
        for company in companies:
            add_audit_log(company.id, 'BATCH_CREATE', user_id, item)
        
        cache.delete_memoized(get_companies)
        
        return jsonify({
            "message": f"Created {len(companies)} companies",
            "company_ids": [c.id for c in companies]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in batch_create_companies: {str(e)}")
        raise APIError(str(e))

@company_api.route('/health')
@limiter.exempt
def health_check():
    """API health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })