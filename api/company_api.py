from flask import Blueprint, jsonify
from model import Company

company_api = Blueprint('company_api', __name__)

@company_api.route('/companies', methods=['GET'])
def get_companies():
    try:
        companies = Company.query.all()
        company_list = [
            {
                'id': c.id,
                'name': c.name,
                'ticker': c.ticker,
                'industry': c.industry,
                'description': c.description
            }
            for c in companies
        ]
        return jsonify(company_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@company_api.route('/companies/<int:id>', methods=['GET'])
def get_company_by_id(id):
    try:
        company = Company.query.get(id)
        if company:
            company_data = {
                'id': company.id,
                'name': company.name,
                'ticker': company.ticker,
                'industry': company.industry,
                'description': company.description
            }
            return jsonify(company_data), 200
        else:
            return jsonify({'error': f'Company ID {id} not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
