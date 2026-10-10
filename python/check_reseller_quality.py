import pandas as pd
from pathlib import Path


# PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

RESELLER_FILE = DATA_DIR / "FactResellerSales.xlsx"


# LOAD DATA

print("=" * 70)
print("CHECKING FACT RESELLER SALES DATA QUALITY")
print("=" * 70)

df = pd.read_excel(RESELLER_FILE)

print(f"\nTotal rows: {len(df)}")


# 1. FIND ROWS WITH MISSING VALUES

print("\n" + "=" * 70)
print("ROWS WITH MISSING VALUES")
print("=" * 70)

missing_rows = df[df.isnull().any(axis=1)]

print(f"\nRows containing at least one missing value: {len(missing_rows)}")

print("\nMissing values by column:")

missing_counts = df.isnull().sum()

for column, count in missing_counts.items():
    if count > 0:
        print(f"{column}: {count}")


# 2. DISPLAY THE INCOMPLETE ROWS

print("\n" + "=" * 70)
print("INCOMPLETE ROWS")
print("=" * 70)

print(missing_rows.to_string(index=False))


# 3. CHECK DUPLICATES

print("\n" + "=" * 70)
print("DUPLICATE ROWS")
print("=" * 70)

duplicates = df[df.duplicated(keep=False)]

print(f"\nTotal rows involved in duplicates: {len(duplicates)}")

if len(duplicates) > 0:
    print("\nDuplicate rows:")
    print(duplicates.to_string(index=False))
else:
    print("No duplicate rows found.")


# 4. CHECK EXTREME SALES VALUES

print("\n" + "=" * 70)
print("TOP 10 HIGHEST SALES AMOUNTS")
print("=" * 70)

top_sales = df.nlargest(10, "SalesAmount")

print(
    top_sales[
        [
            "ProductKey",
            "ResellerKey",
            "EmployeeKey",
            "SalesOrderNumber",
            "SalesOrderLineNumber",
            "SalesAmount",
            "TotalProductCost",
            "OrderDate"
        ]
    ].to_string(index=False)
)


# 5. CHECK SALES AMOUNT STATISTICS

print("\n" + "=" * 70)
print("SALES AMOUNT STATISTICS")
print("=" * 70)

print(df["SalesAmount"].describe())

print("\n" + "=" * 70)
print("QUALITY CHECK COMPLETED")
print("=" * 70)