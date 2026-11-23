import pandas as pd
import matplotlib.pyplot as plt
import os

# Load cleaned data
df = pd.read_csv("outputs/cleaned_retail_data.csv")

# Convert date column
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create reference date
reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

# Score customers from 1 to 5
rfm["R"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5,
    labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5,
    labels=[1, 2, 3, 4, 5]
).astype(int)

# Combine RFM scores
rfm["RFM_Score"] = rfm["R"].astype(str) + \
                   rfm["F"].astype(str) + \
                   rfm["M"].astype(str)

rfm["Total_Score"] = rfm[["R", "F", "M"]].sum(axis=1)

# Segment customers
def segment_customer(row):
    if row["R"] >= 4 and row["F"] >= 4 and row["M"] >= 4:
        return "Champions"
    elif row["Total_Score"] >= 11:
        return "Loyal Customers"
    elif row["R"] <= 2 and row["F"] >= 3:
        return "At Risk"
    elif row["R"] >= 4 and row["F"] <= 2:
        return "New Customers"
    elif row["Total_Score"] >= 8:
        return "Potential Loyalists"
    else:
        return "Needs Attention"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Export RFM dataset
rfm.to_csv("outputs/rfm_customer_segments.csv", index=False)

# Segment summary
segment_summary = rfm.groupby("Segment").agg(
    Customers=("CustomerID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Total_Revenue=("Monetary", "sum")
).reset_index()

segment_summary["Total_Revenue"] = segment_summary["Total_Revenue"].round(2)

segment_summary.to_csv("outputs/rfm_segment_summary.csv", index=False)

# Plot customer segments
plt.figure(figsize=(10, 6))

segment_counts = rfm["Segment"].value_counts()

segment_counts.plot(kind="bar")

plt.title("Customer Distribution by RFM Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/figures/rfm_segments.png", dpi=300)
plt.show()

# Print results
print("\nRFM ANALYSIS COMPLETED")
print("\nSegment Summary:")
print(segment_summary)

print("\nTotal Customers Segmented:", len(rfm))