# scoring.py
# PURPOSE: Take our 5 KPIs and combine them into ONE
# Financial Health Score (0-100) for each company.
# Then classify each company as Healthy, Watch, or At-Risk.
#
# Think of this like a credit score but for ASX companies.
# This is the "analytical thinking" part that impresses interviewers.

import pandas as pd
import os

# Load our clean master file from Day 2
df = pd.read_csv("data\\processed\\master_financials.csv")

print("Calculating Financial Health Scores...")
print("=" * 45)

# -------------------------------------------------------
# HOW THE SCORING WORKS
# Each KPI is scored from 0-20 points (5 KPIs x 20 = 100 max)
# We compare each company AGAINST THE GROUP
# so the best performer gets 20, worst gets 0
# This is called "min-max normalisation" — a real analytics technique
# -------------------------------------------------------

def score_kpi(series, higher_is_better=True):
    """
    Converts raw KPI values into a 0-20 score.
    higher_is_better = True  → higher value = higher score (e.g. profit margin)
    higher_is_better = False → lower value = higher score (e.g. debt ratio)
    """
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return pd.Series([10] * len(series), index=series.index)

    if higher_is_better:
        score = (series - min_val) / (max_val - min_val) * 20
    else:
        score = (max_val - series) / (max_val - min_val) * 20

    return score.round(2)

# Score each KPI out of 20
# Revenue Growth   — higher is better (growing company)
# Gross Margin     — higher is better (more profitable per sale)
# Net Profit Margin— higher is better (more profit overall)
# Debt to Equity   — LOWER is better (less debt = safer)
# Cashflow Ratio   — higher is better (more real cash coming in)

df["Score_Revenue_Growth"]  = score_kpi(df["Revenue_Growth_%"],    higher_is_better=True)
df["Score_Gross_Margin"]    = score_kpi(df["Gross_Margin_%"],       higher_is_better=True)
df["Score_Net_Margin"]      = score_kpi(df["Net_Profit_Margin_%"],  higher_is_better=True)
df["Score_Debt_to_Equity"]  = score_kpi(df["Debt_to_Equity"],       higher_is_better=False)
df["Score_Cashflow"]        = score_kpi(df["Cashflow_Ratio_%"],     higher_is_better=True)

# Add all 5 scores together for final score out of 100
df["Health_Score"] = (
    df["Score_Revenue_Growth"] +
    df["Score_Gross_Margin"]   +
    df["Score_Net_Margin"]     +
    df["Score_Debt_to_Equity"] +
    df["Score_Cashflow"]
).round(2)

# -------------------------------------------------------
# CLASSIFY each company into 3 categories
# Green  = Healthy  (score 65+)
# Yellow = Watch    (score 40-64)
# Red    = At-Risk  (score below 40)
# -------------------------------------------------------
def classify(score):
    if score >= 65:
        return "Healthy"
    elif score >= 40:
        return "Watch"
    else:
        return "At-Risk"

df["Status"] = df["Health_Score"].apply(classify)

# Sort by Health Score — best to worst
df = df.sort_values("Health_Score", ascending=False).reset_index(drop=True)
df["Rank"] = df.index + 1

# -------------------------------------------------------
# PRINT THE LEAGUE TABLE
# -------------------------------------------------------
print("\n🏆 ASX RETAIL FINANCIAL HEALTH LEADERBOARD\n")
print(f"{'Rank':<5} {'Ticker':<10} {'Health Score':<15} {'Status':<15} {'Net Margin%':<15} {'Debt/Equity':<12} {'Revenue Growth%'}")
print("-" * 85)

for _, row in df.iterrows():
    print(f"{int(row['Rank']):<5} {row['Ticker']:<10} {row['Health_Score']:<15} {row['Status']:<15} {row['Net_Profit_Margin_%']:<15} {row['Debt_to_Equity']:<12} {row['Revenue_Growth_%']}")

# -------------------------------------------------------
# SAVE THE FINAL SCORED FILE
# This is what we'll load into Power BI for the dashboard
# -------------------------------------------------------
df.to_csv("data\\processed\\financial_health_scores.csv", index=False)

print("\n========== SUMMARY ==========")
healthy  = len(df[df["Status"] == "Healthy"])
watch    = len(df[df["Status"] == "Watch"])
at_risk  = len(df[df["Status"] == "At-Risk"])
print(f" Healthy  : {healthy} companies")
print(f" Watch    : {watch} companies")
print(f" At-Risk  : {at_risk} companies")
print("\nSaved to: data/processed/financial_health_scores.csv")
print("==============================")