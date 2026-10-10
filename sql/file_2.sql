USE adventure_works_dw;

ALTER TABLE dim_geography
CHANGE COLUMN StateProvinceName State VARCHAR(100);

ALTER TABLE dim_geography
CHANGE COLUMN CountryRegionCode Country VARCHAR(100);


DESCRIBE dim_geography;


USE adventure_works_dw;

ALTER TABLE dim_product
    CHANGE COLUMN ProductName Product VARCHAR(200);

ALTER TABLE dim_product
    DROP COLUMN ProductCategoryKey;

ALTER TABLE dim_product
    DROP COLUMN StandardCost;

ALTER TABLE dim_product
    DROP COLUMN ListPrice;

ALTER TABLE dim_product
    ADD COLUMN Model VARCHAR(200);

ALTER TABLE dim_product
    ADD COLUMN Subcategory VARCHAR(100);

ALTER TABLE dim_product
    ADD COLUMN Category VARCHAR(100);
    
DESCRIBE dim_product


USE adventure_works_dw;

ALTER TABLE dim_reseller
    ADD COLUMN GeographyKey INT AFTER ResellerKey;
    
DESCRIBE dim_reseller;

USE adventure_works_dw;

ALTER TABLE dim_reseller
    DROP COLUMN AnnualSales;
    
DESCRIBE dim_reseller;

DESCRIBE dim_employee;



USE adventure_works_dw;

ALTER TABLE dim_employee
    DROP COLUMN FirstName,
    DROP COLUMN LastName,
    DROP COLUMN Phone;

ALTER TABLE dim_employee
    ADD COLUMN SalesTerritoryKey INT AFTER ParentEmployeeKey;

ALTER TABLE dim_employee
    ADD COLUMN EmployeeName VARCHAR(200) AFTER SalesTerritoryKey;

ALTER TABLE dim_employee
    ADD COLUMN DepartmentName VARCHAR(150) AFTER EmailAddress;
    
    
DESCRIBE dim_employee;

DESCRIBE dim_sales_territory;

DESCRIBE fact_internet_sales;

DESCRIBE fact_reseller_sales;