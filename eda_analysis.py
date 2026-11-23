
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


file_path = "outputs/cleaned_retail_data.csv"

df = pd.read_csv(file_path)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

os.makedirs("outputs/figures", exist_ok=True)

print("\n========== EDA STARTED ==========")


total_revenue = df["Revenue"].sum()

total_orders = df["InvoiceNo"].nunique()

total_units_sold = df["Quantity"].sum()

total_customers = df["CustomerID"].nunique()

total_products = df["StockCode"].nunique()

average_order_value = total_revenue / total_orders

print("\n========== BUSINESS KPIs ==========")

print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Units Sold: {total_units_sold:,}")
print(f"Unique Customers: {total_customers:,}")
print(f"Unique Products: {total_products:,}")
print(f"Average Order Value: {average_order_value:,.2f}")



df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

print("\n========== MONTHLY REVENUE ==========")

print(monthly_revenue)

plt.figure(figsize=(12, 6))

monthly_revenue.index = monthly_revenue.index.astype(str)

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("outputs/figures/monthly_revenue.png", dpi=300)
plt.show()



top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS ==========")

print(top_products)

plt.figure(figsize=(12, 7))

top_products.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("outputs/figures/top_products.png", dpi=300)
plt.show()



country_revenue = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_countries = country_revenue.head(10)

print("\n========== TOP 10 COUNTRIES ==========")

print(top_countries)

plt.figure(figsize=(12, 7))

top_countries.sort_values().plot(kind="barh")

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig("outputs/figures/top_countries.png", dpi=300)
plt.show()


monthly_orders = (
    df.groupby("Month")["InvoiceNo"]
    .nunique()
    .sort_index()
)

print("\n========== MONTHLY ORDERS ==========")

print(monthly_orders)

plt.figure(figsize=(12, 6))

monthly_orders.index = monthly_orders.index.astype(str)

plt.plot(
    monthly_orders.index,
    monthly_orders.values,
    marker="o"
)

plt.title("Monthly Order Volume")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/figures/monthly_orders.png", dpi=300)
plt.show()


df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

day_revenue = (
    df.groupby("DayOfWeek")["Revenue"]
    .sum()
    .reindex(day_order)
)

print("\n========== REVENUE BY DAY ==========")

print(day_revenue)

plt.figure(figsize=(10, 6))

day_revenue.plot(kind="bar")

plt.title("Revenue by Day of Week")
plt.xlabel("Day")
plt.ylabel("Revenue")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/figures/day_revenue.png", dpi=300)
plt.show()


monthly_revenue.to_csv(
    "outputs/monthly_revenue.csv"
)

top_products.to_csv(
    "outputs/top_products.csv"
)

country_revenue.to_csv(
    "outputs/country_revenue.csv"
)

monthly_orders.to_csv(
    "outputs/monthly_orders.csv"
)

day_revenue.to_csv(
    "outputs/day_revenue.csv"
)


print("\n========== EDA COMPLETED ==========")

print("All charts saved inside outputs/figures/")
print("All analytical summaries exported.")
