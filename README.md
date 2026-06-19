# ASX Retail Financial Health Analysis

An end-to-end data analytics project analysing the financial health of 15 ASX-listed 
retail companies using Python, SQL, and Power BI.

## Project Overview

This project builds a financial health scoring model to identify which ASX retail 
companies are financially healthy, at-risk, or require monitoring. It replicates 
the kind of analysis performed by financial analysts at consulting and advisory firms.

## Tools and Technologies

- Python (yfinance, pandas, sqlalchemy)
- SQL (SQLite)
- Power BI

## Dataset

- 15 ASX-listed retail companies
- Financial data sourced from Yahoo Finance via the yfinance Python library
- Data includes income statements, balance sheets, and cash flow statements

## Project Pipeline
Yahoo Finance API → Python (collect) → Python (clean) → SQL Database → Power BI Dashboard

## Key Steps

**1. Data Collection** collect_data.py

Extracted 3 years of financial statements for 15 ASX retail companies 
using the yfinance library. Data saved as CSV files locally.

**2. Data Cleaning and KPI Engineering** clean_data.py

Cleaned raw financial data and engineered 5 key performance indicators:
- Revenue Growth %
- Gross Margin %
- Net Profit Margin %
- Debt to Equity Ratio
- Operating Cash Flow Ratio

**3. Financial Health Scoring** scoring.py

Built a weighted scoring model using min-max normalisation to score each 
company out of 100 across the 5 KPIs. Companies classified as:
- Healthy (65+)
- Watch (40-64)
- At-Risk (below 40)

**4. SQL Database** load_to_sql.py

Loaded processed data into a SQLite database using SQLAlchemy. 
Wrote analytical SQL queries to segment, rank and compare companies.

**5. Power BI Dashboard**

Built a 3-page interactive dashboard:
- Page 1: Executive Overview — leaderboard and health distribution
- Page 2: Company Deep Dive — interactive slicer with KPI cards
- Page 3: Sector Insights — margin comparisons and debt vs profit scatter plot

## Key Findings

1. Revenue size does not equal financial health — Woolworths ($69B revenue) 
   ranks last due to a high debt-to-equity ratio of 3.58

2. Healthy companies average 11.84% net profit margin vs 
   At-Risk companies averaging -0.76%

3. Smaller specialty retailers (UNI.AX, PMV.AX, NCK.AX) outperform 
   large supermarkets on every financial health metric

4. 7 out of 15 ASX retail companies are flagged as At-Risk, 
   suggesting broad financial pressure across the retail sector

## Project Structure
asx-retail-financial-analysis/

├── scripts/

│   ├── collect_data.py

│   ├── clean_data.py

│   ├── scoring.py

│   └── load_to_sql.py

├── data/

│   └── processed/

│       ├── master_financials.csv

│       └── financial_health_scores.csv

└── README.md

## Author

Bachelor of Information Technology Graduate
Seeking junior and graduate data analyst roles in Australia
