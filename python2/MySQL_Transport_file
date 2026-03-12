import pandas as pd
from sqlalchemy import create_engine
import os

# ── PATHS ─────────────────────────────────────────────────────────────
# Relative paths used — works on any machine without changes
INPUT_PATH = os.path.join("output", "supply_chain_clean.csv")

# ── LOAD CLEAN CSV ─────────────────────────────────────────────────────
df = pd.read_csv(INPUT_PATH)

print(f"Loaded : {df.shape}")

# ── CONNECT TO MYSQL ───────────────────────────────────────────────────
# Replace YOUR_PASSWORD with your actual MySQL root password before running

DB_PASSWORD = "your_password_here"


engine = create_engine(
    f"mysql+mysqlconnector://root:{DB_PASSWORD}@localhost/olist_supply_chain"
)

# ── LOAD INTO MYSQL ────────────────────────────────────────────────────


df.to_sql("supply_chain", con=engine, if_exists="replace", index=False)

print(f" Done — {len(df)} rows loaded into MySQL table 'supply_chain'")
