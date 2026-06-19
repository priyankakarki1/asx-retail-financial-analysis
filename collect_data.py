# collect_data.py
# PURPOSE: Connect to Yahoo Finance and download financial data
# for 15 ASX retail companies, then save them as CSV files

import yfinance as yf
import pandas as pd
import os

# -------------------------------------------------------
# STEP 1: Define our list of ASX retail companies
# These are real companies listed on the Australian Stock Exchange
# The .AX suffix tells Yahoo Finance these are ASX-listed stocks
# -------------------------------------------------------
asx_retail = [
    "WOW.AX",   # Woolworths
    "COL.AX",   # Coles
    "WES.AX",   # Wesfarmers
    "JBH.AX",   # JB Hi-Fi
    "HVN.AX",   # Harvey Norman
    "MYR.AX",   # Myer
    "SUL.AX",   # Super Retail Group
    "NCK.AX",   # Nick Scali
    "PMV.AX",   # Premier Investments
    "ADH.AX",   # Adairs
    "KGN.AX",   # Kogan
    "TPW.AX",   # Temple & Webster
    "UNI.AX",   # Universal Store
    "BBN.AX",   # Baby Bunting
    "DMP.AX",   # Domino's Pizza
]

# -------------------------------------------------------
# STEP 2: Create folders to save our data
# raw/ = untouched data straight from Yahoo Finance
# -------------------------------------------------------
os.makedirs("data/raw", exist_ok=True)

# -------------------------------------------------------
# STEP 3: Loop through each company and download their data
# We pull 3 financial statements for each company:
#   - Income Statement (revenue, profit)
#   - Balance Sheet (assets, debts)
#   - Cash Flow Statement (actual cash movement)
# -------------------------------------------------------
successful = []
failed = []

for ticker in asx_retail:
    try:
        print(f"Downloading {ticker}...")
        stock = yf.Ticker(ticker)

        income = stock.financials        # Revenue, Gross Profit, Net Income
        balance = stock.balance_sheet    # Assets, Liabilities, Equity
        cashflow = stock.cashflow        # Operating Cash Flow

        # Only save if we actually got data back
        if income.empty:
            print(f"   No data for {ticker}, skipping...")
            failed.append(ticker)
            continue

        # Save each statement as a separate CSV file
        income.to_csv(f"data/raw/{ticker}_income.csv")
        balance.to_csv(f"data/raw/{ticker}_balance.csv")
        cashflow.to_csv(f"data/raw/{ticker}_cashflow.csv")

        successful.append(ticker)
        print(f"   Saved {ticker}")

    except Exception as e:
        print(f"   Error with {ticker}: {e}")
        failed.append(ticker)

# -------------------------------------------------------
# STEP 4: Print a summary of what we collected
# -------------------------------------------------------
print("\n========== SUMMARY ==========")
print(f" Successfully downloaded: {len(successful)} companies")
print(f" Failed: {len(failed)} companies")
if failed:
    print(f"   Failed tickers: {failed}")
print("Data saved to: data/raw/")
print("==============================")