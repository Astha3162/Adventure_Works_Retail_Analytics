import pandas as pd
from pathlib import Path


# 1. DEFINE FILE PATHS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DIM_FILE = DATA_DIR / "DimTables.xlsx"
INTERNET_SALES_FILE = DATA_DIR / "FactInternetSales.xlsx"
RESELLER_SALES_FILE = DATA_DIR / "FactResellerSales.xlsx"



# 2. LOAD DIMENSION TABLES

print("=" * 70)
print("LOADING DIMENSION TABLES")
print("=" * 70)

dim_tables = pd.read_excel(
    DIM_FILE,
    sheet_name=None
)

print("\nDimension sheets found:")
for sheet_name in dim_tables:
    print(f"- {sheet_name}")


# 3. DISPLAY DIMENSION TABLE INFORMATION

print("\n" + "=" * 70)
print("DIMENSION TABLE DETAILS")
print("=" * 70)

for sheet_name, df in dim_tables.items():

    print(f"\n{'-' * 70}")
    print(f"TABLE: {sheet_name}")
    print(f"{'-' * 70}")

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nMissing values:")
    missing = df.isnull().sum()

    missing_found = False

    for column, count in missing.items():
        if count > 0:
            print(f"  - {column}: {count}")
            missing_found = True

    if not missing_found:
        print("  No missing values")



# 4. LOAD INTERNET SALES

print("\n" + "=" * 70)
print("LOADING FACT INTERNET SALES")
print("=" * 70)

internet_sales = pd.read_excel(INTERNET_SALES_FILE)

print(f"\nRows    : {internet_sales.shape[0]}")
print(f"Columns : {internet_sales.shape[1]}")

print("\nColumns:")
for column in internet_sales.columns:
    print(f"  - {column}")



# 5. LOAD RESELLER SALES

print("\n" + "=" * 70)
print("LOADING FACT RESELLER SALES")
print("=" * 70)

reseller_sales = pd.read_excel(RESELLER_SALES_FILE)

print(f"\nRows    : {reseller_sales.shape[0]}")
print(f"Columns : {reseller_sales.shape[1]}")

print("\nColumns:")
for column in reseller_sales.columns:
    print(f"  - {column}")


# 6. CHECK MISSING VALUES

print("\n" + "=" * 70)
print("MISSING VALUE CHECK")
print("=" * 70)


def check_missing_values(df, table_name):

    print(f"\n{table_name}")

    missing = df.isnull().sum()

    if missing.sum() == 0:
        print("No missing values found.")
    else:
        for column, count in missing.items():
            if count > 0:
                print(f"{column}: {count}")


check_missing_values(
    internet_sales,
    "Fact Internet Sales"
)

check_missing_values(
    reseller_sales,
    "Fact Reseller Sales"
)

for sheet_name, df in dim_tables.items():
    check_missing_values(
        df,
        sheet_name
    )



# 7. CHECK DUPLICATES

print("\n" + "=" * 70)
print("DUPLICATE CHECK")
print("=" * 70)


def check_duplicates(df, table_name):

    duplicate_count = df.duplicated().sum()

    print(
        f"{table_name}: "
        f"{duplicate_count} duplicate rows"
    )


check_duplicates(
    internet_sales,
    "Fact Internet Sales"
)

check_duplicates(
    reseller_sales,
    "Fact Reseller Sales"
)

for sheet_name, df in dim_tables.items():
    check_duplicates(
        df,
        sheet_name
    )



# 8. CHECK DATA TYPES

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

print("\nFact Internet Sales:")
print(internet_sales.dtypes)

print("\nFact Reseller Sales:")
print(reseller_sales.dtypes)



# 9. DISPLAY SAMPLE DATA

print("\n" + "=" * 70)
print("SAMPLE DATA")
print("=" * 70)

print("\nFact Internet Sales - First 5 rows:")
print(internet_sales.head())

print("\nFact Reseller Sales - First 5 rows:")
print(reseller_sales.head())


# 10. BASIC SALES STATISTICS

print("\n" + "=" * 70)
print("BASIC SALES STATISTICS")
print("=" * 70)

print("\nInternet Sales:")
print(
    internet_sales["SalesAmount"].describe()
)

print("\nReseller Sales:")
print(
    reseller_sales["SalesAmount"].describe()
)



# 11. END

print("\n" + "=" * 70)
print("DATA EXPLORATION COMPLETED")
print("=" * 70)