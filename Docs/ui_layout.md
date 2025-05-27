# Ethiopia Capital Market Data Platform  
## UI Layout Notes  

**Date:** May 25, 2025  
**Version:** 1.0  
**Author:** Abel

---

## 📌 Objective  
To define clean, minimal, vibe-coded page layouts and user flows for the Ethiopia Capital Market Data Platform prototype — ensuring a professional, easy-for-the-eye UI that focuses on essential data points only.

---

## 📌 UI Design Guidelines  
- **Minimalist and mobile-friendly layout**
- Use clean white/gray backgrounds with one accent color
- Limit displayed data per view — prioritize clarity over quantity
- Use Bootstrap spacing (`p-2`, `m-3`, `rounded`, `shadow-sm`)
- Charts: one chart per page/tab where possible  
- Keep navigation simple, clean text-based

---

## 📌 Page Layout Descriptions  

---

### 📖 1️⃣ Dashboard Page  

**Purpose**: Quick market overview, easy access to top movers, and macro highlights.

**Sections**
- **Header**: `Ethiopia Capital Market` (centered)
- **Search Bar**: Centered under header
- **Market Summary Card**:  
  - Total Companies  
  - Market Cap  
  - Last Updated  
- **Top 3 Movers Cards**:  
  - Company Name  
  - Current Price  
  - % Change  
- **Macro Highlight Preview**:  
  - GDP Growth  
  - Inflation Rate  
  - 'View All' button  

---

### 📖 2️⃣ Company Details Page  

**Purpose**: Focus view for individual company data.

**Sections**
- **Company Header**: Name, Ticker, Current Price badge
- **Tabs**:
  - Overview: Company Description, recent news
  - Key Financial Data: Table (Revenue, Net Profit, Debt-to-Equity), Bar chart
  - Price Data: Line Chart (10-day stock prices), Volume Bar chart
- **Action Buttons**:
  - Back to Dashboard
  - (Disabled Compare button placeholder)

---

### 📖 3️⃣ Macroeconomic Indicators Page  

**Purpose**: Show macro indicators trends cleanly.

**Sections**
- **Header**: 'Macro Indicators'
- **Date Range Filter**
- **Line Chart**: GDP Growth (toggle for other indicators)
- **Data Table**: 12-month indicator values
- **Back Button**

---

### 📖 4️⃣ Search Results Page  

**Purpose**: Display companies matching a search query.

**Sections**
- **Search Field**
- **Result Cards**:  
  - Company Name  
  - Ticker  
  - Current Price  
  - 'View Details' button  

---

### 📖 5️⃣ Navbar  

**Purpose**: Site-wide navigation

**Links**
- Dashboard  
- Companies  
- Macro Indicators  
- Market Overview  
- Login (optional)

---

## 📌 UI Component List  

| Component         | Pages Where Used               |
|:-----------------|:--------------------------------|
| Market Summary Card | Dashboard |
| Company Card      | Dashboard, Search Results |
| Stock Price Chart | Company Details |
| Financial Table   | Company Details |
| Line Chart        | Macroeconomic Indicators |
| Search Bar        | Dashboard, Search |
| Navbar            | All pages |
| 'View Details' Button | Search Results |
| Tabs (Bootstrap)  | Company Details |
| Back Button       | Company, Macro pages |

---

## 📌 Bilingual Labels (JSON Draft)

```json
{
  "dashboard": "Dashboard",
  "companies": "Companies",
  "macro_indicators": "Macro Indicators",
  "search": "Search",
  "financials": "Financials",
  "price_data": "Price Data",
  "overview": "Overview",
  "market_overview": "Market Overview",
  "view_details": "View Details"
}
########

Color & Style Vibe

Background: #ffffff (white) or #f7f7f7 (light gray)
Text: #333333 (dark charcoal)
Accent Color: Deep Blue #0047AB or Green #28a745
Chart lines: Thin, subtle grid lines
Max one chart per screen/tab
Space generously — no clutter