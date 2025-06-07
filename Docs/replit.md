# 📊 Ethiopia Capital Market Data Platform — Replit Upgrade Plan  

**Date:** 2025-05-27  
**Owner:** Abel  

Hey — I’m working on advancing a Capital Market Data Platform prototype for Ethiopia’s emerging securities exchange market.
The goal is to build an accessible, clean, multi-purpose platform that provides reliable financial, economic, and business data fo

## 🎯 Project Goal

Build a centralized, accessible digital platform providing **reliable financial, economic, and business data for Ethiopia’s capital market** — targeting:
- 🏦 Investors (institutional & retail)  
- 📊 Financial analysts  
- 📚 Researchers  
- 📑 Consultants  
- 📈 Business journalists  
- 📄 Policy advisors  

---

## 📌 Current Focus  

Create a modern, mobile-friendly, multi-purpose platform offering:
- Real-time and historical stock prices  
- Company financial data (Revenue, EBITDA, Net Profit, Debt-to-Equity etc.)  
- Macroeconomic indicators (GDP Growth, Inflation, Interest Rate, FX Reserves etc.)  
- Download tools for CSV & Excel data  
- Public dashboards and company profiles  
- User registration/authentication  
- Clean, vibe-coded, minimalist UI  

---

## 🔧 Tech Structure (Prototype Completed)

- **Backend:**  
  - Python 3.10+  
  - Flask + Flask-RESTful  
  - SQLAlchemy ORM  
  - SQLite (scalable to PostgreSQL)  
  - JWT for user authentication  
  - Flask-Bcrypt for password hashing  

- **Frontend:**  
  - HTML5  
  - CSS (Bootstrap 5)  
  - Chart.js for data visualizations  
  - Vanilla JS for AJAX, dynamic content  
  - Multi-page template structure  

- **APIs Built:**  
  - `/companies`  
  - `/stocks/<company_id>`  
  - `/financials/<company_id>`  
  - `/macro_indicators`  
  - Download endpoints for CSV/Excel  
  - User registration/login JWT auth  

- **Current Pages:**  
  - Market Overview  
  - Company Financials  
  - Macro Indicators  
  - Home Landing Page (summary cards + news)  
  - Data Download pages  

---

## 🚀 What I Want to Do Next (on Replit)

1. Polish the UI into a modern dashboard layout (AdminLTE, Bootstrap Dashboard vibe — minimalist, mobile-friendly)
2. Add **dynamic business & economy news feed** (RSS integration or CSV-based prototype)
3. **Add more diverse economic, trade & financial data types** to macro indicators:
   - External sector: FX Reserves, Trade Balance, Current Account  
   - Financial system: Total Loans, Deposits, NPL Ratio  
   - Additional macro stats as needed  
4. Add **Top Movers and Losers section** to the Market Overview
5. Build a **central Data Download Center page** for authenticated users
6. Implement an **Admin-only Upload API and dashboard** (CSV upload for now)
7. Prepare for **Heroku or AWS deployment**

---

## 💎 Bonus Enhancements  

- 📊 Optimize API query performance  
- 📁 Reorganize frontend folder structure (move to modular `templates/partials/`)  
- 📦 Modularize API blueprints cleanly by resource type  
- 📥 Improve download UX:  
  - Progress indicator on long downloads  
  - Refine multi-variable selection  
  - Option to queue/download multiple CSVs at once  
- 👥 Add **role-based permissions** (Admin, User) for future subscription features  
- 📱 Add optional mobile dashboard optimization using Shadcn or Tailwind CSS  
- 📜 Setup automated data import from scheduled external API calls or FTP uploads (prototype stage: CSV batch imports)

---

## 📦 GitHub Repository  

**Repo:** https://github.com/abela-21/ethiopia-capital-market-platform.git


---

## 🔖 Final Note  

All core features, APIs, and frontends are working and tested via Postman, browser console logs, and Flask debug server.

I’m now ready to polish, scale up, and extend this on **Replit** 🚀.
