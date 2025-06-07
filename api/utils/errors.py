from flask import jsonify

class APIError(Exception):
    """Custom API Exception"""
    def __init__(self, message, status_code=400, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or status_code
        super().__init__(self.message)

    def to_dict(self):
        return {
            'error': {
                'code': self.error_code,
                'message': self.message
            }
        }

def init_error_handlers(app):
    """Initialize error handlers"""
    @app.errorhandler(APIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': {'code': 404, 'message': 'Not found'}}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': {'code': 500, 'message': 'Internal server error'}}), 500