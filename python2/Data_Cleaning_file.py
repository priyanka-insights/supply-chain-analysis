import pandas as pd
import os

# ── PATHS ─────────────────────────────────────────────────────────────
# Relative paths used — works on any machine without changes
INPUT_PATH  = os.path.join("output", "master_raw.csv")
OUTPUT_PATH = os.path.join("output")

df = pd.read_csv(INPUT_PATH)

print(f"Loaded : {df.shape}")

# ── STEP 1: UNDERSTAND ORDER STATUS FIRST ─────────────────────────────
# Before filtering, always SEE what values exist
# Never filter blindly

print("\n=== ORDER STATUS COUNTS ===")
print(df["order_status"].value_counts())


# ── STEP 2: FILTER ONLY DELIVERED ORDERS ──────────────────────────────
# We only keep 'delivered' orders
# Only delivered orders have actual delivery date
# Without actual delivery date, delay calculation is impossible

df = df[df["order_status"] == "delivered"]

print(f"\nAfter filtering delivered only : {df.shape}")

# ── STEP 3: CONVERT DATE COLUMNS TO DATETIME ──────────────────────────
# Right now all date columns are plain text strings
# Python can't do math on strings
# We convert them so Python understands these are actual dates

date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col])

print(f"\nDate columns converted.")
print(f"\nData types now:")
print(df.dtypes)


# ── STEP 4: FEATURE ENGINEERING ───────────────────────────────────────
# These 8 columns don't exist in raw data
# We create them from existing columns using business logic
# This is where analyst adds value — not just loading data

# 1. delay_days — how many days late was each order?
#    Positive = late, Negative = delivered early, Zero = on time
df["delay_days"] = (
    df["order_delivered_customer_date"] -
    df["order_estimated_delivery_date"]
).dt.days

# 2. is_delayed — simple binary flag
#    1 = delayed, 0 = on time or early
df["is_delayed"] = (df["delay_days"] > 0).astype(int)

# 3. order_month — extract month number from purchase date
#    1=Jan, 2=Feb ... 12=Dec
df["order_month"] = df["order_purchase_timestamp"].dt.month

# 4. order_year — extract year
df["order_year"] = df["order_purchase_timestamp"].dt.year

# 5. is_festive — Nov and Dec are festive/peak season in Brazil
#    1 = festive month, 0 = normal month
df["is_festive"] = df["order_month"].isin([11, 12]).astype(int)

# 6. delivery_time — actual days taken from purchase to delivery
df["delivery_time"] = (
    df["order_delivered_customer_date"] -
    df["order_purchase_timestamp"]
).dt.days

# 7. estimated_time — days promised to customer from purchase
df["estimated_time"] = (
    df["order_estimated_delivery_date"] -
    df["order_purchase_timestamp"]
).dt.days

# 8. penalty_cost — financial loss for delayed orders
#    Assumption: 10% of order value per delayed order
#    On time orders = 0 penalty
df["penalty_cost"] = df.apply(
    lambda row: row["total_price"] * 0.10 if row["is_delayed"] == 1 else 0,
    axis=1
)

print("=== 8 NEW COLUMNS CREATED ===")
print(df[["delay_days", "is_delayed", "order_month", "order_year",
          "is_festive", "delivery_time", "estimated_time",
          "penalty_cost"]].head(10))

print(f"\nShape after engineering : {df.shape}")


# ── STEP 5: SANITY CHECK ON NEW COLUMNS ───────────────────────────────
# Always verify your engineered columns make business sense
# Numbers should feel reasonable — if something looks wrong, it is wrong

print("\n=== SANITY CHECK ===")
print(f"Total orders                  : {len(df)}")
print(f"Delayed orders                : {df['is_delayed'].sum()}")
print(f"Delay rate                    : {round(df['is_delayed'].mean() * 100, 2)}%")
print(f"\nAvg delay days (delayed only) : {round(df[df['is_delayed']==1]['delay_days'].mean(), 1)} days")
print(f"Max delay days                : {df['delay_days'].max()} days")
print(f"Min delay days                : {df['delay_days'].min()} days")
print(f"\nFestive orders                : {df['is_festive'].sum()}")
print(f"Non-festive orders            : {(df['is_festive']==0).sum()}")
print(f"\nTotal penalty cost            : R$ {round(df['penalty_cost'].sum(), 2)}")
print(f"Avg penalty per delayed order : R$ {round(df[df['is_delayed']==1]['penalty_cost'].mean(), 2)}")

print(f"\nNull values in new columns:")
print(df[["delay_days", "is_delayed", "delivery_time", "penalty_cost"]].isnull().sum())


# ── STEP 6: DROP NULLS AND SAVE ───────────────────────────────────────
# Drop rows with null delay_days or delivery_time
# These orders had missing dates even after filtering — unusable

print(f"\nBefore dropping nulls : {df.shape}")
df = df.dropna(subset=["delay_days", "delivery_time"])
print(f"After dropping nulls  : {df.shape}")

# Reset index after dropping rows
df = df.reset_index(drop=True)

# Save final clean file
os.makedirs(OUTPUT_PATH, exist_ok=True)
df.to_csv(os.path.join(OUTPUT_PATH, "supply_chain_clean.csv"), index=False)

print(f"\n supply_chain_clean.csv saved")
print(f"Final clean shape : {df.shape}")
print(f"\nColumn list:")
print(list(df.columns))
