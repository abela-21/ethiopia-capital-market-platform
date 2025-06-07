from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.utils.cache import cache
from api.utils.limiter import limiter
from api.utils.errors import init_error_handlers

def init_api(app):
    """Initialize API components"""
    if app is None:
        app = Flask(__name__)
    
    # Register API blueprints
    from api.company_api import company_api
    from api.stock_api import stock_api
    from api.market_api import market_api
    from api.financials_api import financials_api
    from api.macro_api import macro_api
    from api.auth_api import auth_api
    from api.download_api import download_api
    
    # Register blueprints with URL prefixes
    blueprints = [
        (company_api, '/api/v1'),
        (stock_api, '/api/v1'),
        (market_api, '/api/v1'),
        (financials_api, '/api/v1'),
        (macro_api, '/api/v1'),
        (auth_api, '/api/v1'),
        (download_api, '/api/v1')
    ]
    
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
    
    return app