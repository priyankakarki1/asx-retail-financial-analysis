# load_to_sql.py
# PURPOSE: Load our cleaned and scored data into a real SQL database.
# We use SQLite — a lightweight database that lives as a single file.
# This lets us query our data using real SQL just like at work.

import pandas as pd
from sqlalchemy import create_engine, text

# -------------------------------------------------------
# STEP 1: Create the database
# -------------------------------------------------------
db_path = "data\\processed\\asx_financials.db"
engine = create_engine(f"sqlite:///{db_path}")

print("Loading data into SQL database...")
print("=" * 45)

# -------------------------------------------------------
# STEP 2: Load our two CSV files as SQL tables
# -------------------------------------------------------
master = pd.read_csv("data\\processed\\master_financials.csv")
scored = pd.read_csv("data\\processed\\financial_health_scores.csv")

# Rename columns to be SQL-friendly (replace % with _pct)
master.columns = master.columns.str.replace("%", "pct").str.replace(" ", "_")
scored.columns = scored.columns.str.replace("%", "pct").str.replace(" ", "_")

master.to_sql("master_financials", engine, if_exists="replace", index=False)
scored.to_sql("health_scores",     engine, if_exists="replace", index=False)

print("Table 'master_financials' loaded successfully")
print("Table 'health_scores' loaded successfully")

# Confirm column names loaded correctly
print("\nColumns in health_scores table:")
with engine.connect() as conn:
    result = conn.execute(text("PRAGMA table_info(health_scores)"))
    for row in result:
        print(f"  {row[1]}")

# -------------------------------------------------------
# STEP 3: Run SQL queries
# -------------------------------------------------------
print("\n" + "=" * 45)
print("RUNNING SQL QUERIES")
print("=" * 45)

with engine.connect() as conn:

    # QUERY 1: Full leaderboard
    print("\nQUERY 1: Company Leaderboard (Best to Worst)")
    print("-" * 45)
    result = conn.execute(text("""
        SELECT Rank, Ticker, Health_Score, Status,
               Net_Profit_Margin_pct,
               Debt_to_Equity,
               Revenue_Growth_pct
        FROM health_scores
        ORDER BY Rank ASC
    """))
    rows = result.fetchall()
    print(f"{'Rank':<6} {'Ticker':<10} {'Score':<10} {'Status':<12} {'NetMargin%':<12} {'Debt/Eq':<10} {'RevGrowth%'}")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]:<6} {row[1]:<10} {row[2]:<10} {row[3]:<12} {row[4]:<12} {row[5]:<10} {row[6]}")

    # QUERY 2: At-Risk companies only
    print("\nQUERY 2: At-Risk Companies")
    print("-" * 45)
    result = conn.execute(text("""
        SELECT Ticker, Health_Score, Net_Profit_Margin_pct, Debt_to_Equity
        FROM health_scores
        WHERE Status = 'At-Risk'
        ORDER BY Health_Score ASC
    """))
    rows = result.fetchall()
    for row in rows:
        print(f"  {row[0]:<10} Score: {row[1]:<8} NetMargin: {row[2]:<8} Debt/Eq: {row[3]}")

    # QUERY 3: Average KPIs by health status group
    print("\nQUERY 3: Average KPIs by Health Status")
    print("-" * 45)
    result = conn.execute(text("""
        SELECT Status,
               COUNT(*) as Companies,
               ROUND(AVG(Revenue_Growth_pct), 2)    as Avg_Rev_Growth,
               ROUND(AVG(Gross_Margin_pct), 2)      as Avg_Gross_Margin,
               ROUND(AVG(Net_Profit_Margin_pct), 2) as Avg_Net_Margin,
               ROUND(AVG(Debt_to_Equity), 2)        as Avg_Debt_Equity
        FROM health_scores
        GROUP BY Status
        ORDER BY Avg_Net_Margin DESC
    """))
    rows = result.fetchall()
    print(f"{'Status':<12} {'Count':<8} {'RevGrowth%':<12} {'GrossMargin%':<14} {'NetMargin%':<12} {'Debt/Eq'}")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<8} {row[2]:<12} {row[3]:<14} {row[4]:<12} {row[5]}")

    # QUERY 4: Top 5 healthiest companies
    print("\nQUERY 4: Top 5 Healthiest Companies")
    print("-" * 45)
    result = conn.execute(text("""
        SELECT Ticker, Health_Score, Status,
               Gross_Margin_pct, Cashflow_Ratio_pct
        FROM health_scores
        ORDER BY Health_Score DESC
        LIMIT 5
    """))
    rows = result.fetchall()
    for row in rows:
        print(f"  {row[0]:<10} Score: {row[1]:<8} {row[2]:<12} GrossMargin: {row[3]}%  CashFlow: {row[4]}%")

print("\n" + "=" * 45)
print(f"Database saved to: {db_path}")
print("=" * 45)