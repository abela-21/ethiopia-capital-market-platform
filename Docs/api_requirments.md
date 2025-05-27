# Ethiopia Capital Market Data Platform  
## API Requirements Document  

**Date:** May 25, 2025  
**Version:** 1.0  
**Author:** [Your Name]

---

## 📌 1. General API Requirements  

- **Protocol**: RESTful API, using `GET` for data retrieval and `POST` for searches and user actions.  
- **Response Format**: JSON, structured as:
  - **Arrays** for lists (e.g., stocks for Chart.js)
  - **Objects** for single record or summary data (e.g., company profile)  
- **Error Handling**:
  - `400 Bad Request`: Invalid inputs (e.g., malformed dates)
  - `404 Not Found`: Missing resources (e.g., invalid company ID)
  - `500 Internal Server Error`: Database or server failures
- **Performance**: Optimized for small dataset (50 stock rows, 15 financial rows, 12 macro rows), targeting < 1s response time
- **Localization**: English responses by default; Amharic optional if future data includes localized fields
- **Security**: HTTPS in deployment per [ECMA Laws](https://ecma.gov.et/)
- **Scalability**: Endpoints designed for future ESX API integration using flexible query patterns

---

## 📌 2. Feature-Specific Requirements  

Organized by platform feature (as per prototype scope)

---

### 🔹 Core Features

#### 2.1 Real-Time Stock Prices  
- **Purpose**: Display latest stock price for each company  
- **Source**: `Stock` and `Company` tables  
- **Requirements**:
  - Return: `company_id`, `ticker`, `name`, `close`, `date`, `volume`
  - Optional: Include percentage change from prior day’s close  

**Example**
```json
{
  "company_id": 1,
  "ticker": "WGB",
  "name": "Wegagen Bank",
  "close": 53.00,
  "date": "2025-04-10",
  "volume": 5200
}

2.2 Historical Price Data

Purpose: Show 10+ day stock price history for Chart.js
Source: Stock table
Requirements:
Fetch by company_id
Optional date_from / date_to query params
Default: 10 latest records if no dates provided
Validate YYYY-MM-DD format
Example

[
  {
    "id": 1,
    "company_id": 1,
    "date": "2025-04-01",
    "open": 50.0,
    "close": 51.5,
    "high": 52.0,
    "low": 49.0,
    "volume": 5000
  }
]
2.3 Company Profiles

Purpose: Show company details for company pages and search
Source: Company table
Requirements:
Fetch all or by id
Return: id, name, ticker, industry, description
Example

{
  "id": 1,
  "name": "Wegagen Bank",
  "ticker": "WGB",
  "industry": "Banking",
  "description": "Leading commercial bank in Ethiopia."
}
2.4 Market Overview

Purpose: Show dashboard summary
Source: Company and Stock tables
Requirements:
Return: total_companies, market_cap, last_updated
Market cap = latest close price × assumed shares
Example

{
  "total_companies": 5,
  "market_cap": 1500000,
  "last_updated": "2025-04-10"
}
2.5 Search Functionality

Purpose: Support autocomplete for company names/tickers
Source: Company table
Requirements:
POST /search with JSON body { "query": "Weg" }
Return: Array of matching id, name, ticker, industry
Validate: non-empty query
Example

[
  {
    "id": 1,
    "name": "Wegagen Bank",
    "ticker": "WGB",
    "industry": "Banking"
  }
]
🔹 Additional Tabs
2.6 Key Financial Data

Purpose: Show yearly financial metrics for 3 years
Source: Financials table
Requirements:
Fetch by company_id
Optional year filter (e.g., 2024)
Default: All 3 years if no year provided
Example

[
  {
    "year": 2023,
    "revenue": 600000000,
    "net_profit": 50000000,
    "debt_to_equity": 2.0
  }
]
2.7 Macroeconomic Indicators

Purpose: Show macro trends over 12 months
Source: MacroIndicators table
Requirements:
Optional date_from / date_to query params
Return: gdp_growth, inflation_rate, interest_rate, etb_usd, etb_eur, etc.
Example

[
  {
    "date": "2024-05-01",
    "gdp_growth": 6.5,
    "inflation_rate": 20.0,
    "interest_rate": 7.0
  }
]
🔹 Optional: User Authentication
2.8 Register

POST /users/register

Request

{
  "username": "newuser",
  "email": "test@email.com",
  "password": "plaintext"
}
Response

{
  "message": "User registered",
  "user_id": 1
}
2.9 Login

POST /users/login

Request

{
  "username": "newuser",
  "password": "plaintext"
}
Response

{
  "message": "Login successful",
  "token": "jwt_token_here"
}
📌 3. Proposed Endpoints Summary

Method	Endpoint	Purpose
GET	/companies	Get all companies
GET	/companies/<int:id>	Get single company
GET	/stocks/<int:company_id>	Get stock data with optional dates
GET	/financials/<int:company_id>	Get financial data with optional year
GET	/macro_indicators	Get macro data with optional dates
POST	/search	Search by company name/ticker
GET	/market	Get market summary
POST	/users/register (optional)	User registration
POST	/users/login (optional)	User login
📌 4. Technical Specifications

Framework: Flask-RESTful, Flask-SQLAlchemy
Validation: Use reqparse for query parameters and request body validation
Data Types:
Integers: id, company_id, year, volume
Floats: Stock prices, financial metrics, macro indicators
Strings: name, ticker, industry, description, username, email
Dates: YYYY-MM-DD
Error Messages: Specific and clear (e.g., “Company ID 999 not found.”)
Testing: All endpoints tested via Postman