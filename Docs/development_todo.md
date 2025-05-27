# Ethiopia Capital Market Data Platform  
## Development To-Do List (Sprint 1)

**Date:** May 26, 2025  
**Sprint:** Sprint 1 (Weeks 5–12)  
**Version:** 1.1  
**Author:** Abel

---

## 📌 Objective  

Track development progress for Sprint 1, covering core backend APIs, frontend dashboard layout, stock charts, and search functionality.

---

## 📅 Sprint 1 Backend Status  

### 📦 Backend: API Development (Developer)

| Task | Status | Notes |
|:----------------------------------------------------|:--------|:----------------------------|
| Create `/companies` GET endpoint                    | ✅ Done | Tested in Postman |
| Create `/companies/<int:id>` GET endpoint           | ✅ Done | 200 + 404 handled |
| Create `/stocks/<company_id>` GET endpoint w/ filters | ✅ Done | Date range tested |
| Create `/market` GET endpoint                       | ✅ Done | Market cap + date validated |
| Test all backend APIs via Postman                   | ✅ Done | Test JSON collection exported |
| Push working backend APIs to GitHub                 | ✅ Done | Clean repo state |

---

## 📅 Remaining Sprint 1 Frontend Tasks  

| Task | Status |
|:----------------------------------------------------------|:--------|
| Design clean Dashboard Page layout (HTML/Bootstrap)        | 🔜 |
| Build Market Summary Card on Dashboard                     | 🔜 |
| Build Top 3 Movers cards                                    | 🔜 |
| Integrate Search Bar with autocomplete                      | 🔜 |
| Create Stock Price Line Chart (Chart.js)                    | 🔜 |
| Build Search Results Page layout                            | 🔜 |
| Connect frontend AJAX calls to backend APIs                 | 🔜 |
| Test frontend display and data rendering                    | 🔜 |
| Push frontend code to GitHub                                 | 🔜 |
| Test API + UI integration end-to-end                         | 🔜 |
| Commit and push final Sprint 1 code                          | 🔜 |
| Update `sprint_plan.md` and `development_todo.md` status     | 🔜 |

---

## 📦 Deliverables Completed  

- ✅ Backend API endpoints working  
- ✅ Postman Test Collection exported  
- ✅ Test results logged  
- ✅ Code pushed to GitHub  

---

**Next Phase:**  
✅ Move to Sprint 1 Frontend Development (Dashboard page scaffolding)

