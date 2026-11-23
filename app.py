#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 13:15:19 2026

@author: chiranthansateesh
"""


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# Load data
data_path = "outputs/cleaned_retail_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_path)
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# Sidebar
st.sidebar.title("Retail Analytics")
st.sidebar.markdown("### Sales Dashboard")
st.sidebar.write("Dataset: Online Retail")

# Title
st.title("Retail Sales & Customer Behavior Analysis")
st.markdown("Interactive analysis of retail transactions, sales trends and customer purchasing patterns.")

# KPIs
total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_units = df["Quantity"].sum()
avg_order_value = total_revenue / total_orders if total_orders else 0

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Revenue", f"£{total_revenue:,.2f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Customers", f"{total_customers:,}")
c4.metric("Units Sold", f"{total_units:,}")
c5.metric("Average Order Value", f"£{avg_order_value:,.2f}")

st.divider()

# Monthly revenue
st.subheader("Monthly Revenue Trend")

monthly = (
    df.groupby(df["InvoiceDate"].dt.to_period("M"))["Revenue"]
    .sum()
    .reset_index()
)

monthly["InvoiceDate"] = monthly["InvoiceDate"].astype(str)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(monthly["InvoiceDate"], monthly["Revenue"], marker="o")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (£)")
ax.set_title("Monthly Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Two columns
col1, col2 = st.columns(2)

# Top products
with col1:
    st.subheader("Top 10 Products by Revenue")

    products = (
        df.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    products.plot(kind="barh", ax=ax)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("Product")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Country revenue
with col2:
    st.subheader("Top 10 Countries by Revenue")

    countries = (
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    countries.plot(kind="barh", ax=ax)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("Country")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()

# Weekday revenue
st.subheader("Revenue by Day of the Week")

weekday_order = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()

weekday_sales = (
    df.groupby("DayOfWeek")["Revenue"]
    .sum()
    .reindex(weekday_order)
)

fig, ax = plt.subplots(figsize=(10, 4))
weekday_sales.plot(kind="bar", ax=ax)
ax.set_ylabel("Revenue (£)")
ax.set_xlabel("Day")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Data table
st.divider()
st.subheader("Transaction Data Preview")
st.dataframe(df.head(100), use_container_width=True)

st.caption("Built using Python, Pandas, Matplotlib and Streamlit.")
