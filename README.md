#  Supply Chain Delay Analysis
### End-to-End Data Analytics Project | Olist Brazil E-Commerce Dataset

---

##  Project Overview

This project analyzes delivery delays in a Brazilian e-commerce supply chain using the **Olist dataset from Kaggle**. The goal is to identify *why* deliveries get delayed, *where* the problem is worst, and *how much* it costs the business — using a full analytics stack from raw data to interactive dashboard.

**Business Question:**
> Which states, seasons, and seller regions are driving delivery delays — and what is the financial and customer satisfaction impact?

---

##  Tech Stack

| Tool | Purpose |
|---|---|
| Python (Pandas) | Data loading, cleaning, feature engineering, EDA |
| MySQL | Data storage and business SQL queries |
| Power BI | Interactive dashboard and scenario modeling |
| Excel | Summary reporting |

---

##  Project Structure

```
supply-chain-analysis/
│
├── python2/
│   ├── Data_Loading_file.py         # Step 1 — Merge 5 raw files into master
│   ├── Data_Cleaning_file.py        # Step 2 — Clean data + feature engineering
│   ├── EDA_file.py                  # Step 3 — Exploratory data analysis + charts
│   └── MySQL_Transport_file.py      # Step 4 — Load clean CSV into MySQL
│
├── 01_ontime_vs_delayed.png         # Chart 1 — On time vs Delayed orders
├── 02_state_delay_rate.png          # Chart 2 — Top 10 states by delay rate
├── 03_festive_vs_normal.png         # Chart 3 — Festive vs Normal season
├── 04_monthly_trend.png             # Chart 4 — Monthly delay trend
├── 05_delay_vs_review.png           # Chart 5 — Delay duration vs review score
├── 06_seller_state_delay.png        # Chart 6 — Seller state delay rate
│
├── analysis_queries.sql             # Step 5 — 7 business SQL queries
├── Supply_Chain_Analysis.pbix       # Step 6 — Power BI dashboard (4 pages)
├── Supply_Chain_Analysis.xlsx       # Step 7 — Excel summary report
└── README.md
```

---

##  Project Pipeline

```
Raw CSV Files (5 files)
        ↓
  Data_Loading_file.py       →  master_raw.csv
        ↓
  Data_Cleaning_file.py      →  supply_chain_clean.csv
        ↓
  EDA_file.py                →  6 charts (PNG)
        ↓
  MySQL_Transport_file.py    →  MySQL table: supply_chain
        ↓
  analysis_queries.sql       →  7 business queries
        ↓
  Power BI / Excel           →  Interactive dashboard
```

---

##  Dataset

**Source:** [Olist Brazilian E-Commerce Dataset — Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

**Files Used (5 of 9):**

| File | Description |
|---|---|
| olist_orders_dataset.csv | Order status, purchase & delivery timestamps |
| olist_order_items_dataset.csv | Price, freight, seller per order |
| olist_customers_dataset.csv | Customer state |
| olist_order_reviews_dataset.csv | Review score per order |
| olist_sellers_dataset.csv | Seller state |

> **Why only 5 files?** Only columns relevant to the business question were included. Unused files (products, payments, geolocation, etc.) were excluded to keep the analysis focused.

---

##  Data Cleaning & Feature Engineering

Only **delivered** orders were kept — cancelled, shipped, or processing orders cannot have a delay calculated without an actual delivery date.

**8 new columns created:**

| Column | Logic |
|---|---|
| `delay_days` | Actual delivery date − Estimated delivery date |
| `is_delayed` | 1 if delay_days > 0, else 0 |
| `order_month` | Month extracted from purchase timestamp |
| `order_year` | Year extracted from purchase timestamp |
| `is_festive` | 1 if month is November or December (Brazil peak season) |
| `delivery_time` | Actual days from purchase to delivery |
| `estimated_time` | Promised days from purchase to estimated delivery |
| `penalty_cost` | 10% of order value for delayed orders, 0 for on-time |

> **Note:** The 10% penalty rate is an assumption used for financial modeling purposes. It is not a contractual figure from the dataset.

---

##  Key Findings

### 1. Overall Delay Rate
- **96,470 delivered orders** analyzed
- **6,534 orders delayed** — delay rate of **6.8%**
- Average delay duration: **10.6 days**
- Total estimated penalty cost: **R$ 98,600**

### 2. State-Level Performance
- **AL (Alagoas)** has the highest delay rate at **21.4%** — more than 3× the national average
- **MA, SE, PI, CE** also above 13% delay rate
- **SP and RJ** have the highest absolute financial loss despite lower delay rates — due to high order volume

### 3. Festive Season Impact (Nov–Dec)
- Festive season delay rate: **10.3%** vs Normal season: **6.2%**
- Festive season review score: **4.03** vs Normal: **4.18**
- November–December consistently underperforms — logistics capacity is not scaling with demand

### 4. Delay vs Customer Satisfaction
- On-time orders average review score: **4.29 / 5**
- 1–3 day delay: drops to **3.29**
- 4–7 day delay: drops to **2.11**
- 8+ day delay: drops below **1.70**
- Every week of additional delay causes measurable, compounding satisfaction loss

### 5. Seller State Performance
- **MA sellers** have the highest delay rate at **19.07%** among seller states
- SP and RJ sellers — despite being the largest volume states — maintain relatively lower delay rates

---

##  SQL Analysis (7 Queries)

| # | Query | Type |
|---|---|---|
| 1 | Overall business health summary | Basic |
| 2 | State-wise delay ranking | Basic |
| 3 | Festive vs Normal season comparison | Intermediate |
| 4 | Monthly trend analysis | Intermediate |
| 5 | Running cumulative delays | Advanced (Window Function) |
| 6 | Month-over-month delay change | Advanced (LAG Window Function) |
| 7 | Priority customer list for support team | Advanced (CTE + JOIN) |

---

##  Power BI Dashboard (4 Pages)

| Page | What It Shows |
|---|---|
| **Overview** | High-level KPIs, monthly trend, top states by delay rate and financial loss |
| **State Performance** | State-level drill-down with delay rate vs financial loss comparison |
| **Seasonality Analysis** | Festive vs normal season delay rate and review score |
| **Financial Impact** | Penalty cost by state, monthly trend by year, scenario modeling with delay reduction slicer |

> **Key DAX Feature:** The Financial Impact page includes a **Delay Reduction % slicer** that dynamically recalculates projected savings — allowing operations teams to model the financial benefit of improving delivery performance.

---

## ▶ How to Run

### Step 1 — Install Dependencies
```bash
pip install pandas sqlalchemy mysql-connector-python matplotlib seaborn
```

### Step 2 — Run Python Pipeline (in order)
```bash
python python2/Data_Loading_file.py
python python2/Data_Cleaning_file.py
python python2/EDA_file.py
python python2/MySQL_Transport_file.py
```

### Step 3 — MySQL Setup
```sql
CREATE DATABASE olist_supply_chain;
```
Then run `MySQL_Transport_file.py` to load the clean CSV into the table.

### Step 4 — SQL Queries
Open `analysis_queries.sql` in MySQL Workbench and run queries individually or all at once.

### Step 5 — Power BI
Open `Supply_Chain_Analysis.pbix` in Power BI Desktop. Data is already loaded — no reconnection needed unless you want to refresh from MySQL.

### MySQL Password
Before running `MySQL_Transport_file.py`, replace `your_password_here` with your actual MySQL password:
```python
DB_PASSWORD = "your_actual_password"
```

---

##  Business Recommendations

1. **Prioritize AL, MA, SE logistics partners** — these states have delay rates 2–3× the national average and need immediate vendor review
2. **Pre-position inventory in October** before festive season demand spike to reduce the Nov–Dec delay surge
3. **Proactive customer outreach for orders delayed 4+ days** — review scores drop sharply at this threshold, and early communication can retain customers
4. **Audit MA-based sellers** — 19% seller-side delay rate suggests fulfilment issues originating before shipping
5. **Target 20% delay reduction** — the Power BI scenario model shows this would recover approximately R$ 20K in penalty costs annually

---

##  Author

**Priyanka Chaudhary**
Data Analyst | Python • SQL • Power BI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/priyanka-chaudhary775/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/priyanka-insights)

---

##  License

This project uses publicly available data from Kaggle under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

