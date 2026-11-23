
import pandas as pd
import numpy as np
import os

input_path = "data/Online Retail.xlsx"
output_dir = "outputs"

os.makedirs(output_dir, exist_ok=True)



df = pd.read_excel(input_path, engine="openpyxl")

original_rows = len(df)

print("Original dataset loaded:", original_rows)



df.columns = df.columns.str.strip()



duplicate_count = df.duplicated().sum()

df = df.drop_duplicates().copy()

print("Duplicates removed:", duplicate_count)



df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)

df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"], errors="coerce"
)



df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()

cancellation_mask = df["InvoiceNo"].str.startswith("C", na=False)

negative_quantity_mask = df["Quantity"] < 0

cancellations = df[cancellation_mask].copy()

returns = df[negative_quantity_mask].copy()

print("Cancellation invoice records:", len(cancellations))
print("Negative quantity records:", len(returns))



sales_df = df[~cancellation_mask].copy()
sales_df = sales_df[
    (sales_df["Quantity"] > 0) &
    (sales_df["UnitPrice"] > 0)
].copy()


sales_df = sales_df[
    sales_df["InvoiceDate"].notna()
].copy()



sales_df["Revenue"] = (
    sales_df["Quantity"] * sales_df["UnitPrice"]
)


sales_df["Description"] = (
    sales_df["Description"].astype("string").str.strip()
)

sales_df["Country"] = (
    sales_df["Country"].astype("string").str.strip()
)


print("\n========== CLEANING SUMMARY ==========")

print("Original records:", original_rows)
print("After duplicate removal:", len(df))
print("Primary sales records:", len(sales_df))
print("Cancellation records:", len(cancellations))
print("Return records:", len(returns))

print("\nMissing values in cleaned sales data:")
print(sales_df.isnull().sum())

print("\nRevenue statistics:")
print(sales_df["Revenue"].describe())



sales_df.to_csv(
    os.path.join(output_dir, "cleaned_retail_data.csv"),
    index=False
)

cancellations.to_csv(
    os.path.join(output_dir, "cancellation_records.csv"),
    index=False
)

returns.to_csv(
    os.path.join(output_dir, "return_records.csv"),
    index=False
)


cleaning_log = pd.DataFrame({
    "Metric": [
        "Original Records",
        "Duplicate Records Removed",
        "Records After Duplicate Removal",
        "Cancellation Records",
        "Negative Quantity Records",
        "Final Sales Records"
    ],
    "Value": [
        original_rows,
        duplicate_count,
        len(df),
        len(cancellations),
        len(returns),
        len(sales_df)
    ]
})

cleaning_log.to_csv(
    os.path.join(output_dir, "cleaning_log.csv"),
    index=False
)

print("\n========== EXPORT COMPLETED ==========")

print("Cleaned sales data saved.")
print("Cancellation records saved.")
print("Return records saved.")
print("Cleaning log saved.")

print("\nPhase 2 completed successfully!")

