# Financial Transactions Dashboard

An interactive Streamlit app for exploring and visualizing a financial transactions dataset, with a mock-up chatbot and an IQR-based outlier detector.

## 🎯 Highlights
- **Dashboard & charts:** time series, histograms/boxplots, category/merchant breakdowns, heatmaps.
- **Interactive controls:** drop-downs, sliders, and filters inside pages.
- **Mock-up chatbot:** one-click Q&A for common questions (total spend, top merchants/categories, payment mix, outliers, date range).
- **Outlier detection (IQR):** transparent, robust rule for skewed financial data; preview & CSV download.

---

## 📦 Requirements
- Python 3.10.11 
- See `requirements.txt` for Python packages

---

## 🚀 Quick Start
1. **Clone / unzip** this project

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```
streamlit run Home.py
```

## 📂 Project Structure
```
.
├─ Home.py                       # Home page (links to other pages)
├─ financial_transactions.csv    # Provided dataset 
├─ pages/
│  ├─ 1_Dashboard_Analytics.py   # KPIs + charts + heatmaps
│  ├─ 2_Data_Exploration.py      # Schema, nulls, uniques, describe, quick filter
│  ├─ 3_Mockup_Chatbot.py        # Button-based dataset Q&A
│  └─ 4_Outlier_Detection.py     # IQR-based outlier detection (preview & download)
├─ requirements.txt
└─ README.md

```

## 📎 Data schema (expected)
- `transaction_id` (string)
- `date` (datetime / parseable)
- `amount` (numeric)
- `category`, `merchant`, `payment_method`, `account_type`, `transaction_type`, `description` (strings)
# financial-transactions-dashboard
