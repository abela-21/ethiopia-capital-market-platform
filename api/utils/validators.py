from urllib.parse import urlparse
import re

def validate_company_data(data):
    """Validate company data"""
    errors = []
    
    # Required fields validation
    required_fields = {
        'name': str,
        'ticker': str,
        'industry': str
    }
    
    for field, field_type in required_fields.items():
        if field not in data:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(data[field], field_type):
            errors.append(f"Invalid type for {field}")
    
    # Ticker format validation
    if 'ticker' in data and not re.match(r'^[A-Z]{2,5}$', data['ticker']):
        errors.append("Ticker must be 2-5 capital letters")
    
    # Website format validation if provided
    if 'website' in data and data['website']:
        try:
            result = urlparse(data['website'])
            if not all([result.scheme, result.netloc]):
                errors.append("Invalid website URL format")
        except:
            errors.append("Invalid website URL")
    
    return errors