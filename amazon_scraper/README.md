# 🛍️ Amazon Product Scraper & QA Testing Suite

## 📌 Project Overview

This project is a mini e-commerce simulation that scrapes product details from Amazon using Selenium and presents the results through a Django-based web interface. It includes a mock payment gateway and a REST API to store and simulate payment transactions. 

The focus of this project is **end-to-end QA testing** — combining **manual**, **automation**, and **API testing** practices.

---

## 🚀 Features

- 🔍 Search Amazon products using Selenium automation
- 🖥️ Display results on a Django web page
- 💳 Mock payment gateway (Card / UPI / QR)
- 📤 Submit and store transactions via REST API
- ✅ Manual test cases, bug reports, and test plan
- 🤖 Automation testing using Selenium
- 📮 API testing using Postman

---

## 🧪 Testing Strategy

### ✅ Manual Testing
- Functional & UI testing
- Test cases written in Excel (`QA_Test_Cases.xlsx`)
- Bugs documented with severity (`QA_Bug_Report.xlsx`)

### ✅ Automation Testing
- Automated test script (`test_search_product.py`) to validate product search
- Selenium WebDriver used for browser automation

### ✅ API Testing
- Postman used to test `POST /api/transactions/`
- Collection available in `Postman_API_Tests/`

---

## 🧱 Tech Stack

| Component      | Technology         |
|----------------|--------------------|
| Backend        | Django (Python)    |
| Web Scraping   | Selenium           |
| Database       | PostgreSQL         |
| API Testing    | Postman            |
| Manual Testing | Excel + Word       |
| Automation     | Selenium (Python)  |
| IDE            | Jupyter Notebook   |

---

## 🗃️ Folder Structure

amazon_scraper/
├── core Django project files
├── QA_Testing/
│   ├── Test_Plan_Document.docx
│   ├── Selenium_Automation/
│   │   └── test_search_product.py
│   ├── QA_Test_Cases.xlsx
│   ├── QA_Bug_Report.xlsx
│   ├── Postman_API_Tests/
│   │   └── Mock Payment API Testing.postman_collection.json
│   └── Screenshots/        # Optional
└── README.md



---

## 🧠 What I Learned

- End-to-end QA workflow (test planning to bug reporting)
- Automation testing using Selenium
- REST API testing with Postman
- Manual testing approach with real test scenarios
- Django web development and form handling
- Documenting and organizing a real-world QA project

---

## 👩‍💻 Author

**Sunakshi Gaikwad**  

---

## 📎 License

This project is for educational and demonstration purposes only.

