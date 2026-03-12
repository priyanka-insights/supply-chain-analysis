import pandas as pd
import matplotlib.pyplot as plt
import os

# ── PATHS ─────────────────────────────────────────────────────────────
# Relative paths used — works on any machine without changes
INPUT_PATH   = os.path.join("output", "supply_chain_clean.csv")
OUTPUT_PATH  = os.path.join("output", "eda_charts")
SAVE_PATH    = os.path.join("output")

os.makedirs(OUTPUT_PATH, exist_ok=True)

df = pd.read_csv(INPUT_PATH)

print(f"Loaded : {df.shape}")

# ── ANALYSIS 1: OVERALL BUSINESS HEALTH ───────────────────────────────
# This gives you the headline numbers for your entire project
# These are the exact figures you mention in interviews

total_orders        = len(df)
delayed_orders      = df["is_delayed"].sum()
delay_rate          = round(df["is_delayed"].mean() * 100, 2)
avg_delay_days      = round(df[df["is_delayed"] == 1]["delay_days"].mean(), 1)
total_penalty       = round(df["penalty_cost"].sum(), 2)
avg_review_delayed  = round(df[df["is_delayed"] == 1]["review_score"].mean(), 2)
avg_review_ontime   = round(df[df["is_delayed"] == 0]["review_score"].mean(), 2)

print("=" * 45)
print("      OVERALL BUSINESS HEALTH SUMMARY")
print("=" * 45)
print(f"Total delivered orders     : {total_orders:,}")
print(f"Delayed orders             : {delayed_orders:,}")
print(f"Delay rate                 : {delay_rate}%")
print(f"Avg delay (when late)      : {avg_delay_days} days")
print(f"Total penalty cost         : R$ {total_penalty:,}")
print(f"Avg review — delayed       : {avg_review_delayed} / 5")
print(f"Avg review — on time       : {avg_review_ontime} / 5")
print("=" * 45)

# ── CHART 1: ON TIME VS DELAYED ───────────────────────────────────────
labels = ["On Time", "Delayed"]
values = [total_orders - delayed_orders, delayed_orders]
colors = ["#2ecc71", "#e74c3c"]

plt.figure(figsize=(8, 5))
bars = plt.bar(labels, values, color=colors, width=0.4, edgecolor="white")

for bar, val in zip(bars, values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 200,
        f"{val:,}",
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

plt.title("On Time vs Delayed Orders", fontsize=14, fontweight="bold")
plt.ylabel("Number of Orders")
plt.ylim(0, max(values) * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "01_ontime_vs_delayed.png"),
            dpi=150, bbox_inches="tight")
plt.close()

print("\n✔ Chart 1 saved — 01_ontime_vs_delayed.png")


# ── ANALYSIS 2: STATE-WISE DELAY RATE ─────────────────────────────────
# Which states have the worst delay problem?
# We look at delay RATE not just volume
# A small state with 50% delay rate is worse than
# a big state with 10% delay rate

state_analysis = df.groupby("customer_state").agg(
    total_orders   = ("order_id", "count"),
    delayed_orders = ("is_delayed", "sum"),
    avg_delay_days = ("delay_days", "mean"),
    total_penalty  = ("penalty_cost", "sum")
).reset_index()

state_analysis["delay_rate"] = round(
    (state_analysis["delayed_orders"] / state_analysis["total_orders"]) * 100, 2
)

state_analysis = state_analysis.sort_values("delay_rate", ascending=False)

print("\n=== TOP 10 STATES BY DELAY RATE ===")
print(state_analysis[["customer_state", "total_orders",
                        "delayed_orders", "delay_rate"]].head(10).to_string())

# ── CHART 2: TOP 10 STATES ─────────────────────────────────────────────
top10_states = state_analysis.head(10)

plt.figure(figsize=(12, 6))
bars = plt.bar(
    top10_states["customer_state"],
    top10_states["delay_rate"],
    color="steelblue",
    edgecolor="white"
)

for bar, rate in zip(bars, top10_states["delay_rate"]):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{rate}%",
        ha="center",
        fontsize=9,
        fontweight="bold"
    )

plt.title("Top 10 States by Delay Rate", fontsize=14, fontweight="bold")
plt.xlabel("Customer State")
plt.ylabel("Delay Rate (%)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "02_state_delay_rate.png"),
            dpi=150, bbox_inches="tight")
plt.close()

print("\n✔ Chart 2 saved — 02_state_delay_rate.png")

state_analysis.to_csv(os.path.join(SAVE_PATH, "state_analysis.csv"), index=False)
print("✔ state_analysis.csv saved")


# ── ANALYSIS 3: FESTIVE VS NORMAL SEASON ──────────────────────────────
# Does Nov-Dec peak season make delays worse?
# We compare delay rate AND review score between both periods

festive_analysis = df.groupby("is_festive").agg(
    total_orders   = ("order_id", "count"),
    delayed_orders = ("is_delayed", "sum"),
    avg_review     = ("review_score", "mean"),
    avg_delay_days = ("delay_days", "mean")
).reset_index()

festive_analysis["delay_rate"]    = round(
    (festive_analysis["delayed_orders"] / festive_analysis["total_orders"]) * 100, 2
)
festive_analysis["avg_review"]     = round(festive_analysis["avg_review"], 2)
festive_analysis["avg_delay_days"] = round(festive_analysis["avg_delay_days"], 2)
festive_analysis["season"]         = festive_analysis["is_festive"].map(
    {0: "Normal Season", 1: "Festive Season"}
)

print("\n=== FESTIVE VS NORMAL SEASON ===")
print(festive_analysis[["season", "total_orders", "delayed_orders",
                          "delay_rate", "avg_review", "avg_delay_days"]].to_string())

# ── CHART 3: SIDE BY SIDE COMPARISON ──────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].bar(
    festive_analysis["season"],
    festive_analysis["delay_rate"],
    color=["#3498db", "#e74c3c"],
    width=0.4,
    edgecolor="white"
)
for i, (rate, count) in enumerate(zip(
    festive_analysis["delay_rate"],
    festive_analysis["total_orders"]
)):
    axes[0].text(i, rate + 0.2, f"{rate}%\n({count:,} orders)",
                 ha="center", fontsize=10, fontweight="bold")

axes[0].set_title("Delay Rate: Festive vs Normal", fontweight="bold")
axes[0].set_ylabel("Delay Rate (%)")
axes[0].set_ylim(0, max(festive_analysis["delay_rate"]) * 1.3)

axes[1].bar(
    festive_analysis["season"],
    festive_analysis["avg_review"],
    color=["#3498db", "#e74c3c"],
    width=0.4,
    edgecolor="white"
)
for i, score in enumerate(festive_analysis["avg_review"]):
    axes[1].text(i, score + 0.05, f"{score} / 5",
                 ha="center", fontsize=10, fontweight="bold")

axes[1].set_title("Avg Review: Festive vs Normal", fontweight="bold")
axes[1].set_ylabel("Average Review Score")
axes[1].set_ylim(0, 5.5)

plt.suptitle("Festive Season Impact on Delays", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "03_festive_vs_normal.png"),
            dpi=150, bbox_inches="tight")
plt.close()

print("\n✔ Chart 3 saved — 03_festive_vs_normal.png")


# ── ANALYSIS 4: MONTHLY TREND ─────────────────────────────────────────
# Is the delay situation getting better or worse over time?
# We look at delay rate month by month across 2017-2018

monthly = df.groupby(["order_year", "order_month"]).agg(
    total_orders   = ("order_id", "count"),
    delayed_orders = ("is_delayed", "sum")
).reset_index()

monthly["delay_rate"] = round(
    (monthly["delayed_orders"] / monthly["total_orders"]) * 100, 2
)

monthly["period"] = (
    monthly["order_year"].astype(str) + "-" +
    monthly["order_month"].astype(str).str.zfill(2)
)

monthly = monthly.sort_values("period").reset_index(drop=True)

# Remove months with less than 100 orders — startup noise
monthly_clean = monthly[monthly["total_orders"] >= 100].copy()

fig, ax1 = plt.subplots(figsize=(16, 6))

ax1.plot(
    monthly_clean["period"],
    monthly_clean["delay_rate"],
    color="#e74c3c",
    linewidth=2.5,
    marker="o",
    markersize=5,
    label="Delay Rate %"
)
ax1.set_ylabel("Delay Rate (%)", color="#e74c3c")
ax1.tick_params(axis="y", labelcolor="#e74c3c")

ax2 = ax1.twinx()
ax2.bar(
    monthly_clean["period"],
    monthly_clean["total_orders"],
    color="#3498db",
    alpha=0.3,
    label="Order Volume"
)
ax2.set_ylabel("Order Volume", color="#3498db")
ax2.tick_params(axis="y", labelcolor="#3498db")

tick_positions = range(0, len(monthly_clean), 2)
ax1.set_xticks(list(tick_positions))
ax1.set_xticklabels(
    [monthly_clean["period"].iloc[i] for i in tick_positions],
    rotation=45,
    ha="right"
)

ax1.set_title("Monthly Delay Rate vs Order Volume (2017-2018)",
              fontsize=14, fontweight="bold")
ax1.set_xlabel("Month")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "04_monthly_trend.png"),
            dpi=150, bbox_inches="tight")
plt.close()

monthly.to_csv(os.path.join(SAVE_PATH, "monthly_trend.csv"), index=False)

print("\n✔ Chart 4 saved — 04_monthly_trend.png")
print("✔ monthly_trend.csv saved")


# ── ANALYSIS 5: DELAY DAYS VS REVIEW SCORE ────────────────────────────
# Does longer delay = worse review score?
# We bucket delay_days into groups and see average review per bucket

delayed_only = df[df["is_delayed"] == 1].copy()

delayed_only["delay_bucket"] = pd.cut(
    delayed_only["delay_days"],
    bins=[0, 3, 7, 14, 30, 200],
    labels=["1-3 days", "4-7 days", "8-14 days", "15-30 days", "30+ days"]
)

bucket_analysis = delayed_only.groupby("delay_bucket", observed=True).agg(
    order_count = ("order_id", "count"),
    avg_review  = ("review_score", "mean")
).reset_index()

bucket_analysis["avg_review"] = round(bucket_analysis["avg_review"], 2)

print("\n=== DELAY SEVERITY VS REVIEW SCORE ===")
print(bucket_analysis.to_string())

# ── CHART 5 ────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(10, 6))

ax2 = ax1.twinx()
ax2.bar(
    bucket_analysis["delay_bucket"].astype(str),
    bucket_analysis["order_count"],
    color="#3498db",
    alpha=0.3,
    label="Order Count"
)
ax2.set_ylabel("Number of Orders", color="#3498db")
ax2.tick_params(axis="y", labelcolor="#3498db")

ax1.plot(
    bucket_analysis["delay_bucket"].astype(str),
    bucket_analysis["avg_review"],
    color="#e74c3c",
    linewidth=2.5,
    marker="o",
    markersize=8,
    label="Avg Review Score",
    zorder=5
)

for i, row in bucket_analysis.iterrows():
    ax1.annotate(
        f"{row['avg_review']}★",
        xy=(i, row["avg_review"]),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        fontsize=10,
        fontweight="bold",
        color="#e74c3c"
    )

ax1.set_ylabel("Average Review Score", color="#e74c3c")
ax1.tick_params(axis="y", labelcolor="#e74c3c")
ax1.set_ylim(1, 4)
ax1.set_xlabel("Delay Severity")
ax1.set_title("How Delay Duration Affects Customer Review Score",
              fontsize=13, fontweight="bold")

ax1.axhline(
    y=4.29,
    color="green",
    linestyle="--",
    linewidth=1.5,
    label="On-Time Avg (4.29)"
)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "05_delay_vs_review.png"),
            dpi=150, bbox_inches="tight")
plt.close()

print("\n✔ Chart 5 saved — 05_delay_vs_review.png")


# ── ANALYSIS 6: SELLER STATE DELAY RATE ───────────────────────────────
# Is delay concentrated in specific seller locations?
# This tells us if the problem is seller-side or logistics-side

seller_state_analysis = df.groupby("seller_state").agg(
    total_orders   = ("order_id", "count"),
    delayed_orders = ("is_delayed", "sum"),
    avg_delay_days = ("delay_days", "mean")
).reset_index()

seller_state_analysis["delay_rate"] = round(
    (seller_state_analysis["delayed_orders"] /
     seller_state_analysis["total_orders"]) * 100, 2
)

# Keep only states with meaningful volume — min 50 orders
seller_state_analysis = seller_state_analysis[
    seller_state_analysis["total_orders"] >= 50
]

seller_state_analysis = seller_state_analysis.sort_values(
    "delay_rate", ascending=False
).head(10)

print("\n=== TOP 10 SELLER STATES BY DELAY RATE ===")
print(seller_state_analysis[["seller_state", "total_orders",
                               "delayed_orders", "delay_rate"]].to_string())

# ── CHART 6 ────────────────────────────────────────────────────────────
plt.figure(figsize=(12, 6))
bars = plt.barh(
    seller_state_analysis["seller_state"],
    seller_state_analysis["delay_rate"],
    color="#e67e22",
    edgecolor="white"
)

for bar, rate in zip(bars, seller_state_analysis["delay_rate"]):
    plt.text(
        bar.get_width() + 0.2,
        bar.get_y() + bar.get_height() / 2,
        f"{rate}%",
        va="center",
        fontsize=9,
        fontweight="bold"
    )

plt.title("Top 10 Seller States by Delay Rate",
          fontsize=14, fontweight="bold")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Seller State")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, "06_seller_state_delay.png"),
            dpi=150, bbox_inches="tight")
plt.close()

# Save EDA summary
eda_summary = df.groupby("customer_state").agg(
    total_orders   = ("order_id", "count"),
    delay_rate     = ("is_delayed", "mean"),
    avg_delay_days = ("delay_days", "mean"),
    avg_review     = ("review_score", "mean"),
    total_penalty  = ("penalty_cost", "sum")
).reset_index()

eda_summary["delay_rate"]     = round(eda_summary["delay_rate"] * 100, 2)
eda_summary["avg_delay_days"] = round(eda_summary["avg_delay_days"], 2)
eda_summary["avg_review"]     = round(eda_summary["avg_review"], 2)
eda_summary["total_penalty"]  = round(eda_summary["total_penalty"], 2)

eda_summary.to_csv(os.path.join(SAVE_PATH, "eda_summary.csv"), index=False)

print("\n✔ Chart 6 saved — 06_seller_state_delay.png")
print("✔ eda_summary.csv saved")
print("\n✔ ALL 6 EDA ANALYSES COMPLETE")
