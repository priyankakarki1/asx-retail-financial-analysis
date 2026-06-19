# clean_data.py
# PURPOSE: Read all raw CSV files, calculate 5 KPIs,
# and save one clean master file ready for analysis.

import pandas as pd
import os

asx_retail = [
    "WOW.AX", "COL.AX", "WES.AX", "JBH.AX", "HVN.AX",
    "MYR.AX", "SUL.AX", "NCK.AX", "PMV.AX", "ADH.AX",
    "KGN.AX", "TPW.AX", "UNI.AX", "BBN.AX", "DMP.AX",
]

# Helper: tries multiple name variations and returns the first match
# This is needed because different companies label rows slightly differently
def get_row(df, options):
    for name in options:
        if name in df.index:
            return df.loc[name].iloc[0]
    return None

def get_row_prev(df, options):
    for name in options:
        if name in df.index:
            return df.loc[name].iloc[1]
    return None

all_companies = []

for ticker in asx_retail:
    try:
        # Load the 3 CSV files for this company
        income   = pd.read_csv(f"data/raw/{ticker}_income.csv",   index_col=0)
        balance  = pd.read_csv(f"data/raw/{ticker}_balance.csv",  index_col=0)
        cashflow = pd.read_csv(f"data/raw/{ticker}_cashflow.csv", index_col=0)

        # --- INCOME STATEMENT ---
        # Revenue = total money made from sales
        revenue_now  = get_row(income,      ["Total Revenue", "Operating Revenue"])
        revenue_prev = get_row_prev(income, ["Total Revenue", "Operating Revenue"])

        # Gross Profit = revenue minus cost of goods sold
        gross_profit = get_row(income, ["Gross Profit"])

        # Net Income = final profit after all expenses and taxes
        net_income = get_row(income, [
            "Net Income",
            "Net Income Common Stockholders",
            "Net Income From Continuing Operation Net Minority Interest"
        ])

        # --- BALANCE SHEET ---
        # Total Debt = all money owed to banks/lenders
        total_debt = get_row(balance, [
            "Total Debt",
            "Long Term Debt And Capital Lease Obligation",
            "Long Term Debt"
        ])

        # Equity = company's own money (what's left after paying all debts)
        equity = get_row(balance, [
            "Stockholders Equity",
            "Common Stock Equity",
            "Total Equity Gross Minority Interest"
        ])

        # --- CASH FLOW ---
        # Operating Cash Flow = actual cash the business generated
        op_cashflow = get_row(cashflow, [
            "Operating Cash Flow",
            "Cash Flow From Continuing Operating Activities",
            "Net Cash Provided By Operating Activities",
            "Cash Flowsfromusedin Operating Activities Direct",
            "Free Cash Flow"
        ])
        

        # Skip company if any value is missing
        missing = []
        if revenue_now  is None: missing.append("revenue_now")
        if revenue_prev is None: missing.append("revenue_prev")
        if gross_profit is None: missing.append("gross_profit")
        if net_income   is None: missing.append("net_income")
        if total_debt   is None: missing.append("total_debt")
        if equity       is None: missing.append("equity")
        if op_cashflow  is None: missing.append("op_cashflow")

        if missing:
            print(f" Skipped {ticker} — missing: {missing}")
            continue

        if equity == 0 or revenue_now == 0:
            print(f" Skipped {ticker} — zero equity or revenue")
            continue

        # --- CALCULATE 5 KPIs ---

        # 1. Revenue Growth % — is the company growing year over year?
        revenue_growth = ((revenue_now - revenue_prev) / abs(revenue_prev)) * 100

        # 2. Gross Margin % — how profitable is each dollar of sales?
        gross_margin = (gross_profit / revenue_now) * 100

        # 3. Net Profit Margin % — how much profit after ALL expenses?
        net_margin = (net_income / revenue_now) * 100

        # 4. Debt to Equity — how much debt vs own money? lower = safer
        debt_to_equity = total_debt / equity

        # 5. Cash Flow Ratio % — is real cash actually coming in?
        cashflow_ratio = (op_cashflow / revenue_now) * 100

        all_companies.append({
            "Ticker":               ticker,
            "Revenue_Billions_AUD": round(revenue_now / 1e9, 2),
            "Revenue_Growth_%":     round(revenue_growth, 2),
            "Gross_Margin_%":       round(gross_margin, 2),
            "Net_Profit_Margin_%":  round(net_margin, 2),
            "Debt_to_Equity":       round(debt_to_equity, 2),
            "Cashflow_Ratio_%":     round(cashflow_ratio, 2),
        })

        print(f"Processed {ticker}")

    except Exception as e:
        print(f" Skipped {ticker} — reason: {e}")

# --- SAVE MASTER FILE ---
df = pd.DataFrame(all_companies)
os.makedirs("data\\processed", exist_ok=True)
df.to_csv("data\\processed\\master_financials.csv", index=False)

print("\n========== SUMMARY ==========")
print(f"Companies processed: {len(df)}")
print("\nPreview of your data:")
print(df.to_string(index=False))
print("\nSaved to: data/processed/master_financials.csv")
print("==============================")