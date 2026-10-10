CREATE DATABASE adventure_works_dw;

USE adventure_works_dw;

USE adventure_works_dw;


-- ADVENTURE WORKS RETAIL ANALYTICS
-- STAR SCHEMA - TABLE CREATION



-- 1. CUSTOMER DIMENSION

CREATE TABLE IF NOT EXISTS dim_customer (
    CustomerKey INT PRIMARY KEY,
    GeographyKey INT,
    CustomerName VARCHAR(200),
    BirthDate DATE,
    MaritalStatus VARCHAR(10),
    Gender VARCHAR(10),
    EmailAddress VARCHAR(200),
    YearlyIncome DECIMAL(15,2),
    Education VARCHAR(100),
    Occupation VARCHAR(100),
    HouseOwnerFlag VARCHAR(10),
    Address VARCHAR(500),
    FirstPurchaseDate DATE,
    Age INT,
    AgeGroup VARCHAR(20)
);



-- 2. GEOGRAPHY / STORE LOCATION DIMENSION

CREATE TABLE IF NOT EXISTS dim_geography (
    GeographyKey INT PRIMARY KEY,
    City VARCHAR(100),
    StateProvinceName VARCHAR(100),
    CountryRegionCode VARCHAR(20),
    PostalCode VARCHAR(20),
    SalesTerritoryKey INT
);



-- 3. PRODUCT DIMENSION

CREATE TABLE IF NOT EXISTS dim_product (
    ProductKey INT PRIMARY KEY,
    ProductName VARCHAR(200),
    ProductSubcategoryKey INT,
    ProductCategoryKey INT,
    Color VARCHAR(50),
    StandardCost DECIMAL(15,2),
    ListPrice DECIMAL(15,2)
);



-- 4. RESELLER DIMENSION

CREATE TABLE IF NOT EXISTS dim_reseller (
    ResellerKey INT PRIMARY KEY,
    ResellerName VARCHAR(200),
    BusinessType VARCHAR(100),
    AnnualSales DECIMAL(18,2)
);



-- 5. EMPLOYEE DIMENSION

CREATE TABLE IF NOT EXISTS dim_employee (
    EmployeeKey INT PRIMARY KEY,
    ParentEmployeeKey INT NULL,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Title VARCHAR(150),
    BirthDate DATE,
    HireDate DATE,
    EmailAddress VARCHAR(200),
    Phone VARCHAR(50)
);



-- 6. SALES TERRITORY DIMENSION

CREATE TABLE IF NOT EXISTS dim_sales_territory (
    SalesTerritoryKey INT PRIMARY KEY,
    SalesTerritoryRegion VARCHAR(100),
    SalesTerritoryCountry VARCHAR(100),
    SalesTerritoryGroup VARCHAR(100)
);



-- 7. FACT INTERNET SALES

CREATE TABLE IF NOT EXISTS fact_internet_sales (
    InternetSalesKey BIGINT AUTO_INCREMENT PRIMARY KEY,

    ProductKey INT,
    CustomerKey INT,
    SalesTerritoryKey INT,

    SalesOrderNumber VARCHAR(50),
    SalesOrderLineNumber INT,

    DiscountAmount DECIMAL(15,2),
    TotalProductCost DECIMAL(15,2),
    SalesAmount DECIMAL(15,2),
    Freight DECIMAL(15,2),

    OrderDate DATE,
    DueDate DATE,
    ShipDate DATE,

    FOREIGN KEY (ProductKey)
        REFERENCES dim_product(ProductKey),

    FOREIGN KEY (CustomerKey)
        REFERENCES dim_customer(CustomerKey),

    FOREIGN KEY (SalesTerritoryKey)
        REFERENCES dim_sales_territory(SalesTerritoryKey)
);



-- 8. FACT RESELLER SALES

CREATE TABLE IF NOT EXISTS fact_reseller_sales (
    ResellerSalesKey BIGINT AUTO_INCREMENT PRIMARY KEY,

    ProductKey INT,
    ResellerKey INT,
    EmployeeKey INT,
    SalesTerritoryKey INT,

    SalesOrderNumber VARCHAR(50),
    SalesOrderLineNumber INT,

    DiscountAmount DECIMAL(15,2),
    TotalProductCost DECIMAL(15,2),
    SalesAmount DECIMAL(15,2),
    Freight DECIMAL(15,2),

    OrderDate DATE,
    DueDate DATE,
    ShipDate DATE,

    FOREIGN KEY (ProductKey)
        REFERENCES dim_product(ProductKey),

    FOREIGN KEY (ResellerKey)
        REFERENCES dim_reseller(ResellerKey),

    FOREIGN KEY (EmployeeKey)
        REFERENCES dim_employee(EmployeeKey),

    FOREIGN KEY (SalesTerritoryKey)
        REFERENCES dim_sales_territory(SalesTerritoryKey)
);
