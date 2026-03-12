import pandas as pd
import os

# ── PATHS ─────────────────────────────────────────────────────────────
# Relative paths used — works on any machine without changes
DATA_PATH   = os.path.join("raw data")
OUTPUT_PATH = os.path.join("output")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ── STEP 1: LOAD ALL 5 FILES ──────────────────────────────────────────
# We selected 5 out of 9 available files
# Selection based on business question — only what we actually need

orders    = pd.read_csv(os.path.join(DATA_PATH, "olist_orders_dataset.csv"))
items     = pd.read_csv(os.path.join(DATA_PATH, "olist_order_items_dataset.csv"))
customers = pd.read_csv(os.path.join(DATA_PATH, "olist_customers_dataset.csv"))
reviews   = pd.read_csv(os.path.join(DATA_PATH, "olist_order_reviews_dataset.csv"))
sellers   = pd.read_csv(os.path.join(DATA_PATH, "olist_sellers_dataset.csv"))

print("=== RAW FILE SHAPES ===")
print(f"Orders    : {orders.shape}")
print(f"Items     : {items.shape}")
print(f"Customers : {customers.shape}")
print(f"Reviews   : {reviews.shape}")
print(f"Sellers   : {sellers.shape}")

# ── STEP 2: QUICK COLUMN CHECK ────────────────────────────────────────
# Before merging we need to know the JOIN KEYS
# What column connects these files to each other?

print("\n=== COLUMN NAMES ===")
print(f"Orders    : {list(orders.columns)}")
print(f"Items     : {list(items.columns)}")
print(f"Customers : {list(customers.columns)}")
print(f"Reviews   : {list(reviews.columns)}")
print(f"Sellers   : {list(sellers.columns)}")

# ── STEP 3: AGGREGATE ITEMS FIRST ─────────────────────────────────────
# Items has multiple rows per order (multi-item orders)
# We collapse it to one row per order before merging
# We only need total price and freight value per order

items_agg = items.groupby("order_id").agg(
    total_price   = ("price", "sum"),
    total_freight = ("freight_value", "sum")
).reset_index()

print(f"\nItems after aggregation : {items_agg.shape}")
# This should now match orders row count — 99,441

# ── STEP 4: MERGE ALL FILES ───────────────────────────────────────────
# We build the master table step by step
# Don't merge all at once — do it one by one so you can catch issues

# Start with orders as the base
df = orders.merge(customers, on="customer_id", how="left")
print(f"\nAfter adding customers  : {df.shape}")

# Add aggregated items
df = df.merge(items_agg, on="order_id", how="left")
print(f"After adding items      : {df.shape}")

# Add reviews — take only what we need
reviews_clean = reviews[["order_id", "review_score"]].drop_duplicates(subset="order_id")
df = df.merge(reviews_clean, on="order_id", how="left")
print(f"After adding reviews    : {df.shape}")

# Add sellers — but first get seller_id from items
seller_map = items[["order_id", "seller_id"]].drop_duplicates(subset="order_id")
df = df.merge(seller_map, on="order_id", how="left")
df = df.merge(sellers, on="seller_id", how="left")
print(f"After adding sellers    : {df.shape}")

print("\n✔ Master dataframe ready")
print(f"Final shape : {df.shape}")
print(f"\nColumns : {list(df.columns)}")

# ── STEP 5: KEEP ONLY USEFUL COLUMNS ──────────────────────────────────
# We drop columns that don't answer our business questions
# Keeping only what we need makes the dataframe clean and fast

columns_to_keep = [
    "order_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "customer_state",
    "total_price",
    "total_freight",
    "review_score",
    "seller_state"
]

df = df[columns_to_keep]

print(f"\nAfter column selection : {df.shape}")
print(f"Columns kept : {list(df.columns)}")

# ── STEP 6: SAVE MASTER RAW FILE ──────────────────────────────────────
# Save this before any cleaning
# Rule: always save raw merged file separately
# If cleaning goes wrong, you don't have to re-run the merge

df.to_csv(os.path.join(OUTPUT_PATH, "master_raw.csv"), index=False)
print("\n master_raw.csv saved to output folder")
print(f"Final shape : {df.shape}")
