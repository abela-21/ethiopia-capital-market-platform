from flask import Flask, render_template, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from api.models.models import db, bcrypt, Company
from flask_jwt_extended import JWTManager
from api import init_api
from api.company_api import company_api
from api.stock_api import stock_api
from api.market_api import market_api
from api.financials_api import financials_api
from api.macro_api import macro_api
from api.auth_api import auth_api
from api.download_api import download_api
from api.utils.errors import init_error_handlers
import os
import logging
from datetime import timedelta
from dotenv import load_dotenv
from config import SQLALCHEMY_DATABASE_URI

# Load environment variables
load_dotenv()


class Config:
    """Base configuration"""

    # Database
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

    # CORS
    CORS_HEADERS = "Content-Type"

    # Debug
    DEBUG = os.getenv("FLASK_ENV") == "development"

    # Template and Static
    TEMPLATE_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "templates"
    )
    STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

    # Cache
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300

    # Rate Limiting
    RATELIMIT_DEFAULT = "200 per day"
    RATELIMIT_STORAGE_URL = "memory://"


def setup_logging(app):
    """Configure logging"""
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.join(app.root_path, "logs"), exist_ok=True)

    log_level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(
        filename=os.path.join(app.root_path, "logs", "app.log"),
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Also log to console in development
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        logging.getLogger("").addHandler(console_handler)


def create_app(config_object=Config):
    """Application factory function"""
    # Create required directories
    for folder in ["logs", "uploads", "static", "templates"]:
        os.makedirs(os.path.join(os.path.dirname(__file__), folder), exist_ok=True)

    app = Flask(
        __name__,
        template_folder=config_object.TEMPLATE_FOLDER,
        static_folder=config_object.STATIC_FOLDER,
    )

    # Load configuration
    app.config.from_object(config_object)

    # Setup logging
    setup_logging(app)

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    cache = Cache(app)

    app.config["RATELIMIT_STORAGE_URL"] = os.getenv(
        "REDIS_URL", "redis://localhost:6379/0"
    )
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day"],
        storage_uri="memory://"
    )

    # Initialize API components
    init_api(app)

    # Initialize error handlers
    init_error_handlers(app)

    # JWT configuration
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        # TODO: Implement token blocklist check with Redis or database
        return False

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token"}), 401

    # Health check endpoint
    @app.route("/health")
    @limiter.exempt
    def health_check():
        """API health check endpoint"""
        try:
            db_status = "connected" if db.engine.pool.checkedout() == 0 else "error"
            return jsonify(
                {
                    "status": "healthy",
                    "database": db_status,
                    "environment": os.getenv("FLASK_ENV", "production"),
                }
            ), 200
        except Exception as e:
            logging.error(f"Health check failed: {str(e)}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    # Frontend routes
    @app.route("/")
    def index():
        """Landing page"""
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        """Main dashboard"""
        return render_template("dashboard.html")

    @app.route("/search-results")
    def search_results():
        """Search results page"""
        return render_template("search_results.html")

    @app.route("/company-details/<int:company_id>")
    def company_details(company_id):
        """Company details page"""
        try:
            company = Company.query.get_or_404(company_id)
            return render_template("company_details.html", company=company)
        except Exception as e:
            logging.error(f"Error fetching company details: {str(e)}")
            return render_template("errors/500.html"), 500

    @app.route("/macro-overview")
    def macro_overview():
        """Macroeconomic overview page"""
        return render_template("macro_overview.html")

    @app.route("/home")
    def home():
        """Home page"""
        return render_template("home.html")

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logging.error(f"Internal server error: {str(error)}")
        return render_template("errors/500.html"), 500

    return app


# Development server configuration
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            logging.info("✅ Database tables created successfully")
        except Exception as e:
            logging.error(f"❌ Error creating database tables: {e}")

    app.run(
        host="0.0.0.0", port=int(os.getenv("PORT", 5001)), debug=app.config["DEBUG"]
    )
