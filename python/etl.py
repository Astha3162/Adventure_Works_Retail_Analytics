import pandas as pd
from pathlib import Path


# 1. PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = BASE_DIR / "processed_data"

PROCESSED_DIR.mkdir(exist_ok=True)


# 2. FILE PATHS

DIM_FILE = DATA_DIR / "DimTables.xlsx"
INTERNET_FILE = DATA_DIR / "FactInternetSales.xlsx"
RESELLER_FILE = DATA_DIR / "FactResellerSales.xlsx"



# 3. START ETL

print("=" * 70)
print("ADVENTURE WORKS - ETL PROCESS")
print("=" * 70)


# 4. LOAD DIMENSION TABLES

print("\nLoading dimension tables...")

dim_tables = pd.read_excel(
    DIM_FILE,
    sheet_name=None
)

dim_customer = dim_tables["DimCustomer"]
dim_employee = dim_tables["DimEmployee"]
dim_geography = dim_tables["DimGeography"]
dim_product = dim_tables["DimProduct"]
dim_reseller = dim_tables["DimReseller"]
dim_sales_territory = dim_tables["DimSalesTerritory"]

print("Dimension tables loaded successfully.")



# 5. LOAD FACT TABLES

print("\nLoading fact tables...")

fact_internet = pd.read_excel(INTERNET_FILE)
fact_reseller = pd.read_excel(RESELLER_FILE)

print("Fact tables loaded successfully.")

print(f"Internet Sales rows : {len(fact_internet)}")
print(f"Reseller Sales rows : {len(fact_reseller)}")


# 6. CLEAN DIMENSION TABLES

print("\nCleaning dimension tables...")


# DimEmployee
# ParentEmployeeKey can legitimately be missing for the
# top-level employee, so we keep the missing value.

dim_employee["ParentEmployeeKey"] = (
    pd.to_numeric(
        dim_employee["ParentEmployeeKey"],
        errors="coerce"
    ).astype("Int64")
)


# DimProduct

# Missing product color is replaced with "Unknown".

dim_product["Color"] = (
    dim_product["Color"]
    .fillna("Unknown")
    .astype(str)
)


# DimSalesTerritory

# One territory has missing descriptive information.
# We replace missing text with "Unknown".

territory_columns = [
    "SalesTerritoryRegion",
    "SalesTerritoryCountry",
    "SalesTerritoryGroup"
]

for column in territory_columns:
    dim_sales_territory[column] = (
        dim_sales_territory[column]
        .fillna("Unknown")
        .astype(str)
    )



# 7. CLEAN INTERNET SALES


print("\nCleaning Fact Internet Sales...")

# Remove exact duplicate rows.
internet_before = len(fact_internet)

fact_internet = fact_internet.drop_duplicates()

internet_removed = internet_before - len(fact_internet)

print(f"Duplicate internet rows removed: {internet_removed}")



# Convert date columns

date_columns = [
    "OrderDate",
    "DueDate",
    "ShipDate"
]

for column in date_columns:
    fact_internet[column] = pd.to_datetime(
        fact_internet[column],
        errors="coerce"
    )


# Convert numeric columns

numeric_columns_internet = [
    "ProductKey",
    "CustomerKey",
    "SalesTerritoryKey",
    "SalesOrderLineNumber",
    "DiscountAmount",
    "TotalProductCost",
    "SalesAmount",
    "Freight"
]

for column in numeric_columns_internet:
    fact_internet[column] = pd.to_numeric(
        fact_internet[column],
        errors="coerce"
    )



# 8. CLEAN RESELLER SALES

print("\nCleaning Fact Reseller Sales...")

reseller_before = len(fact_reseller)


# Remove incomplete sales rows

# These rows have no essential identifiers such as
# ProductKey, ResellerKey, SalesOrderNumber or OrderDate.

required_columns = [
    "ProductKey",
    "ResellerKey",
    "SalesOrderNumber",
    "OrderDate"
]

missing_before = len(fact_reseller)

fact_reseller = fact_reseller.dropna(
    subset=required_columns
)

incomplete_removed = missing_before - len(fact_reseller)

print(f"Incomplete reseller rows removed: {incomplete_removed}")



# Remove exact duplicate rows

before_duplicates = len(fact_reseller)

fact_reseller = fact_reseller.drop_duplicates()

duplicates_removed = (
    before_duplicates - len(fact_reseller)
)

print(f"Duplicate reseller rows removed: {duplicates_removed}")


# Convert date columns

for column in date_columns:
    fact_reseller[column] = pd.to_datetime(
        fact_reseller[column],
        errors="coerce"
    )



# Convert numeric columns

numeric_columns_reseller = [
    "ProductKey",
    "ResellerKey",
    "EmployeeKey",
    "SalesTerritoryKey",
    "SalesOrderLineNumber",
    "DiscountAmount",
    "TotalProductCost",
    "SalesAmount",
    "Freight"
]

for column in numeric_columns_reseller:
    fact_reseller[column] = pd.to_numeric(
        fact_reseller[column],
        errors="coerce"
    )


# 9. CLEAN TEXT COLUMNS

print("\nCleaning text columns...")


def clean_text_columns(df):
    """
    Removes unnecessary spaces from text columns.
    """
    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df


dim_customer = clean_text_columns(dim_customer)
dim_employee = clean_text_columns(dim_employee)
dim_geography = clean_text_columns(dim_geography)
dim_product = clean_text_columns(dim_product)
dim_reseller = clean_text_columns(dim_reseller)
dim_sales_territory = clean_text_columns(
    dim_sales_territory
)

fact_internet = clean_text_columns(fact_internet)
fact_reseller = clean_text_columns(fact_reseller)


# 10. REMOVE UNUSED COLUMNS

# CarrierTrackingNumber is completely empty in Internet Sales
# and is not required for the analytical requirements.

if "CarrierTrackingNumber" in fact_internet.columns:
    fact_internet = fact_internet.drop(
        columns=["CarrierTrackingNumber"]
    )

# CarrierTrackingNumber is also not required for the
# main reseller analysis.

if "CarrierTrackingNumber" in fact_reseller.columns:
    fact_reseller = fact_reseller.drop(
        columns=["CarrierTrackingNumber"]
    )


# 11. CREATE AGE COLUMN IN CUSTOMER DIMENSION

print("\nCreating customer age...")

dim_customer["BirthDate"] = pd.to_datetime(
    dim_customer["BirthDate"],
    errors="coerce"
)

reference_date = pd.Timestamp("2014-12-31")

dim_customer["Age"] = (
    reference_date.year
    - dim_customer["BirthDate"].dt.year
)

birthday_not_reached = (
    (dim_customer["BirthDate"].dt.month > reference_date.month)
    |
    (
        (dim_customer["BirthDate"].dt.month == reference_date.month)
        &
        (dim_customer["BirthDate"].dt.day > reference_date.day)
    )
)

dim_customer.loc[
    birthday_not_reached,
    "Age"
] -= 1


# 12. CREATE AGE GROUP

print("Creating customer age groups...")

age_bins = [
    0,
    25,
    30,
    35,
    40,
    45,
    50,
    60,
    100
]

age_labels = [
    "Under 25",
    "25-30",
    "30-35",
    "35-40",
    "40-45",
    "45-50",
    "50-60",
    "60+"
]

dim_customer["AgeGroup"] = pd.cut(
    dim_customer["Age"],
    bins=age_bins,
    labels=age_labels,
    right=False
)



# 13. RESET INDEXES

dimension_tables = {
    "DimCustomer": dim_customer,
    "DimEmployee": dim_employee,
    "DimGeography": dim_geography,
    "DimProduct": dim_product,
    "DimReseller": dim_reseller,
    "DimSalesTerritory": dim_sales_territory
}

for name, df in dimension_tables.items():
    dimension_tables[name] = df.reset_index(drop=True)

fact_internet = fact_internet.reset_index(drop=True)
fact_reseller = fact_reseller.reset_index(drop=True)


# 14. SAVE PROCESSED DATA

print("\nSaving processed data...")

for name, df in dimension_tables.items():

    output_file = PROCESSED_DIR / f"{name}.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"{name}: {len(df)} rows saved"
    )


fact_internet.to_csv(
    PROCESSED_DIR / "FactInternetSales.csv",
    index=False
)

fact_reseller.to_csv(
    PROCESSED_DIR / "FactResellerSales.csv",
    index=False
)

print(
    f"FactInternetSales: {len(fact_internet)} rows saved"
)

print(
    f"FactResellerSales: {len(fact_reseller)} rows saved"
)


# 15. FINAL ETL SUMMARY

print("\n" + "=" * 70)
print("ETL SUMMARY")
print("=" * 70)

print("\nDimension tables:")

for name, df in dimension_tables.items():
    print(
        f"{name:<25} {len(df):>8} rows"
    )

print("\nFact tables:")

print(
    f"{'FactInternetSales':<25} {len(fact_internet):>8} rows"
)

print(
    f"{'FactResellerSales':<25} {len(fact_reseller):>8} rows"
)

print("\nProcessed files saved to:")
print(PROCESSED_DIR)

print("\n" + "=" * 70)
print("ETL PROCESS COMPLETED SUCCESSFULLY")
print("=" * 70)