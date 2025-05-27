from flask import Flask
from model import db, Company
from api.company_api import company_api
from api.stock_api import stock_api
from api.market_api import market_api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////Users/abela/Downloads/Project X/market.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Register blueprint BEFORE running the app
app.register_blueprint(company_api)

# Register stock API blueprint
app.register_blueprint(stock_api)

# Register market API blueprint
app.register_blueprint(market_api)

@app.route("/")
def index():
    return "Database setup complete."


@app.route("/test-db")
def test_db():
    companies = Company.query.all()
    return {"companies": [c.name for c in companies]}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
