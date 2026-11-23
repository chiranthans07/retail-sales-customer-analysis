#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 15:58:56 2026

@author: chiranthansateesh
"""


# ==========================================
# RETAIL SALES AND CUSTOMER BEHAVIOUR ANALYSIS
# Phase 1: Dataset Loading and Inspection
# ==========================================

import pandas as pd
import numpy as np
import os

file_path = "data/Online Retail.xlsx"


if not os.path.exists(file_path):
    raise FileNotFoundError("Online Retail.xlsx not found in data folder!")


df = pd.read_excel(file_path, engine="openpyxl")

print("\n========== DATASET LOADED SUCCESSFULLY ==========")

print("\nDataset Shape:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


print("\nColumn Names:")
print(df.columns.tolist())


print("\nFirst Five Records:")
print(df.head())


print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())


print("\nDuplicate Records:")
print(df.duplicated().sum())


print("\nUnique Customers:", df["CustomerID"].nunique())
print("Unique Products:", df["StockCode"].nunique())
print("Unique Countries:", df["Country"].nunique())

print("\nTransaction Date Range:")
print("Start:", df["InvoiceDate"].min())
print("End:", df["InvoiceDate"].max())

print("\n========== INSPECTION COMPLETED ==========")















print("\n========== DATA QUALITY SUMMARY ==========")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nUnique Customers:")
print(df["CustomerID"].nunique())

print("\nUnique Products:")
print(df["StockCode"].nunique())

print("\nUnique Countries:")
print(df["Country"].nunique())

print("\nTransaction Period:")
print(df["InvoiceDate"].min())
print(df["InvoiceDate"].max())

print("\nCancelled Invoices:")
print(df["InvoiceNo"].astype(str).str.startswith("C").sum())

print("\nNegative Quantities:")
print((df["Quantity"] < 0).sum())

print("\nZero or Negative Prices:")
print((df["UnitPrice"] <= 0).sum())
