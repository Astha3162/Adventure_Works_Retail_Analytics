import pandas as pd
from pathlib import Path
from getpass import getpass

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL



# 1. PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "processed_data"



# 2. MYSQL CONNECTION DETAILS

USERNAME = "root"
HOST = "localhost"
PORT = 3306
DATABASE = "adventure_works_dw"

PASSWORD = getpass("Enter your MySQL password: ")


connection_url = URL.create(
    "mysql+mysqlconnector",
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DATABASE
)

engine = create_engine(connection_url)



# 3. TEST MYSQL CONNECTION

print("\nTesting MySQL connection...")

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("MySQL connection successful!")

except Exception as error:
    print("\nERROR: Could not connect to MySQL.")
    print(error)
    raise SystemExit



# 4. TABLE MAPPING

tables = [
    ("DimGeography.csv", "dim_geography"),
    ("DimCustomer.csv", "dim_customer"),
    ("DimProduct.csv", "dim_product"),
    ("DimReseller.csv", "dim_reseller"),
    ("DimEmployee.csv", "dim_employee"),
    ("DimSalesTerritory.csv", "dim_sales_territory"),
    ("FactInternetSales.csv", "fact_internet_sales"),
    ("FactResellerSales.csv", "fact_reseller_sales")
]



# 5. CHECK TABLE STATUS

print("\nChecking existing table data...\n")

tables_to_load = []

for file_name, table_name in tables:

    file_path = PROCESSED_DIR / file_name

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        raise SystemExit

    df = pd.read_csv(file_path)

    expected_count = len(df)

    with engine.connect() as connection:
        query = text(f"SELECT COUNT(*) FROM `{table_name}`")
        existing_count = connection.execute(query).scalar()

    print(
        f"{table_name:<25} "
        f"Existing: {existing_count:<8} "
        f"Expected: {expected_count}"
    )

    # Table completely empty
    if existing_count == 0:
        tables_to_load.append((file_name, table_name))

    # Table already contains exactly the expected number of rows
    elif existing_count == expected_count:
        print(f"  -> Already loaded. Skipping {table_name}.")

    # Table contains some but not all rows
    else:
        print(f"\nWARNING: {table_name} contains partial data.")
        print(f"Existing rows : {existing_count}")
        print(f"Expected rows : {expected_count}")
        print("\nLoading stopped to prevent duplicate or incomplete data.")
        raise SystemExit



# 6. CHECK WHETHER EVERYTHING IS ALREADY LOADED

if not tables_to_load:

    print("\n" + "=" * 60)
    print("ALL TABLES ARE ALREADY LOADED.")
    print("=" * 60)

    raise SystemExit


print("\nTables that will be loaded:")

for file_name, table_name in tables_to_load:
    print(f"  -> {table_name}")



# 7. LOAD DATA

print("\n" + "=" * 60)
print("STARTING DATA LOADING")
print("=" * 60)


for file_name, table_name in tables_to_load:

    file_path = PROCESSED_DIR / file_name

    print("\n" + "=" * 60)
    print(f"Loading: {file_name}")
    print(f"Target table: {table_name}")
    print("=" * 60)

    df = pd.read_csv(file_path)

    print(f"Rows read from CSV: {len(df)}")


    
    # Convert date columns

    date_columns = [
        "BirthDate",
        "FirstPurchaseDate",
        "HireDate",
        "OrderDate",
        "DueDate",
        "ShipDate"
    ]

    for column in date_columns:

        if column in df.columns:

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            ).dt.date


  
    # Convert integer columns

    integer_columns = [
        "CustomerKey",
        "GeographyKey",
        "ProductKey",
        "ProductSubcategoryKey",
        "ProductCategoryKey",
        "ResellerKey",
        "EmployeeKey",
        "ParentEmployeeKey",
        "SalesTerritoryKey",
        "SalesOrderLineNumber",
        "Age"
    ]

    for column in integer_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            ).astype("Int64")


   
    # Load into MySQL

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000
    )


    
    # Verify row count

    with engine.connect() as connection:

        query = text(
            f"SELECT COUNT(*) FROM `{table_name}`"
        )

        loaded_count = connection.execute(query).scalar()


    print(f"Rows loaded into MySQL: {loaded_count}")
    print(f"Completed: {table_name}")



# 8. FINAL MYSQL ROW COUNT VALIDATION

print("\n" + "=" * 60)
print("FINAL MYSQL ROW COUNT VALIDATION")
print("=" * 60)


for file_name, table_name in tables:

    with engine.connect() as connection:

        query = text(
            f"SELECT COUNT(*) FROM `{table_name}`"
        )

        count = connection.execute(query).scalar()

    print(f"{table_name:<25} : {count}")



# 9. COMPLETION MESSAGE

print("\n" + "=" * 60)
print("DATA LOADING COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nAll processed CSV files have been loaded")
print("into the adventure_works_dw MySQL database.")