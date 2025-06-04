from flask import Flask, render_template
from model import db, bcrypt, Company
from flask_jwt_extended import JWTManager
from api.company_api import company_api
from api.stock_api import stock_api
from api.market_api import market_api
from api.financials_api import financials_api
from api.macro_api import macro_api
from api.auth_api import auth_api
from api.download_api import download_api


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////Users/abela/Downloads/Project X/market.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Change this in production

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(company_api)
app.register_blueprint(stock_api)
app.register_blueprint(market_api)
app.register_blueprint(financials_api)
app.register_blueprint(macro_api)
app.register_blueprint(auth_api)
app.register_blueprint(download_api)


@app.route("/")
def index():
    return "Database setup complete."


@app.route("/test-db")
def test_db():
    companies = Company.query.all()
    return {"companies": [c.name for c in companies]}


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/search-results")
def search_results():
    return render_template("search_results.html")


@app.route("/company-details/<int:company_id>")
def company_details(company_id):
    company = Company.query.get(company_id)
    if not company:
        return "Company not found", 404
    return render_template("company_details.html", company_id=company_id)


@app.route("/macro-overview")
def macro_overview():
    return render_template("macro_overview.html")


@app.route("/home")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
