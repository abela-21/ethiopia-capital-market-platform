# Ethiopia Capital Market Data Platform  
## Sprint 1 Task Breakdown  

**Date:** May 25, 2025  
**Sprint:** Sprint 1 (Weeks 5–12)  
**Version:** 1.0  
**Author:** [Your Name]

---

## 📌 Objective  

Detailed task-by-task breakdown of Sprint 1 deliverables with role assignments, AI tool support, and expected outputs for each task.

---

## 📅 Sprint 1 Task Table  

| #  | Task Description                                | Role        | AI Tools / Helpers        | Deliverable                                |
|:----|:------------------------------------------------|:------------|:---------------------------|:--------------------------------------------|
| 1  | Set up `/companies` GET API                     | Developer   | Grok, Copilot, Tabnine     | API endpoint returning all companies        |
| 2  | Set up `/companies/<int:id>` GET API            | Developer   | Grok, Copilot               | API endpoint returning single company       |
| 3  | Set up `/stocks/<company_id>` GET API with date filters | Developer   | Grok, Copilot, Tabnine     | API endpoint returning stock data w/ filters|
| 4  | Set up `/market` GET API for market summary     | Developer   | Copilot, Grok               | API endpoint returning market overview data |
| 5  | Test all backend APIs via Postman               | Developer   | —                           | Postman test logs/screenshots               |
| 6  | Push working backend APIs to GitHub             | Developer   | —                           | GitHub commits                              |
| 7  | Design clean Dashboard Page layout (HTML/Bootstrap) | You         | Copilot, Tabnine             | HTML layout file `/templates/dashboard.html`|
| 8  | Build Market Summary Card on Dashboard          | You         | Copilot                     | Card component in HTML/Bootstrap            |
| 9  | Build Top 3 Movers cards                        | You         | Copilot                     | Bootstrap card row with price and % change  |
| 10 | Integrate Search Bar with autocomplete          | You         | Copilot                     | Search bar in header w/ JS autocomplete     |
| 11 | Create Stock Price Line Chart (Chart.js)        | You         | Copilot, Chart.js docs       | Working chart in Dashboard page             |
| 12 | Build Search Results Page layout                | You         | Copilot, Tabnine             | `/templates/search_results.html`            |
| 13 | Connect frontend AJAX calls to backend APIs     | You         | Copilot, Tabnine             | JS scripts + working data fetch calls       |
| 14 | Test frontend display and data rendering        | You         | —                           | Screenshots and local test notes            |
| 15 | Push frontend code to GitHub                    | You         | —                           | GitHub commits                              |
| 16 | Test API + UI integration end-to-end            | Both        | Chrome DevTools              | Working prototype pages with live data      |
| 17 | Commit and push final Sprint 1 code             | Both        | —                           | Finalized repo state on GitHub              |
| 18 | Update `sprint_plan.md` and `development_todo.md` status | You         | Notion, Markdown PDF         | Updated docs and exported PDFs              |

---

## 📌 AI Tools Quick Reference  

| AI Tool        | Use Case                           |
|:---------------|:------------------------------------|
| **GitHub Copilot** | Code generation for Python, HTML, JS |
| **Grok (xAI)**     | Explaining and writing backend API logic |
| **Tabnine**        | JS functions, API requests, AJAX helpers |
| **Chart.js Docs**  | Chart configuration reference      |
| **Chrome DevTools**| Frontend debugging, data checks    |

---

## ✅ Next Step  
Start with **Task #1: Set up `/companies` GET API**

