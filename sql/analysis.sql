USE adventure_works_dw;

-- ADVENTURE WORKS RETAIL ANALYTICS
-- SQL BUSINESS ANALYSIS


-- 1. TOTAL INTERNET SALES

SELECT
    ROUND(SUM(SalesAmount), 2) AS Total_Internet_Sales
FROM fact_internet_sales;


-- 2. TOTAL RESELLER SALES

SELECT
    ROUND(SUM(SalesAmount), 2) AS Total_Reseller_Sales
FROM fact_reseller_sales;


-- 3. COMBINED TOTAL SALES

SELECT
    ROUND(
        (SELECT SUM(SalesAmount)
         FROM fact_internet_sales)
        +
        (SELECT SUM(SalesAmount)
         FROM fact_reseller_sales),
        2
    ) AS Total_Sales;


-- 4. SALES BY SALES TERRITORY

SELECT
    st.SalesTerritoryRegion,
    st.SalesTerritoryCountry,
    ROUND(
        COALESCE(internet.InternetSales, 0)
        +
        COALESCE(reseller.ResellerSales, 0),
        2
    ) AS Total_Sales
FROM dim_sales_territory st
LEFT JOIN
(
    SELECT
        SalesTerritoryKey,
        SUM(SalesAmount) AS InternetSales
    FROM fact_internet_sales
    GROUP BY SalesTerritoryKey
) internet
    ON st.SalesTerritoryKey = internet.SalesTerritoryKey
LEFT JOIN
(
    SELECT
        SalesTerritoryKey,
        SUM(SalesAmount) AS ResellerSales
    FROM fact_reseller_sales
    GROUP BY SalesTerritoryKey
) reseller
    ON st.SalesTerritoryKey = reseller.SalesTerritoryKey
ORDER BY Total_Sales DESC;


-- 5. AVERAGE ORDER VALUE - INTERNET SALES

SELECT
    ROUND(
        SUM(SalesAmount) / COUNT(DISTINCT SalesOrderNumber),
        2
    ) AS Internet_Average_Order_Value
FROM fact_internet_sales;


-- 6. AVERAGE ORDER VALUE - RESELLER SALES

SELECT
    ROUND(
        SUM(SalesAmount) / COUNT(DISTINCT SalesOrderNumber),
        2
    ) AS Reseller_Average_Order_Value
FROM fact_reseller_sales;


-- 7. AVERAGE ORDER VALUE BY SALES TERRITORY

SELECT
    st.SalesTerritoryRegion,
    ROUND(
        SUM(all_sales.SalesAmount)
        / COUNT(DISTINCT all_sales.SalesOrderNumber),
        2
    ) AS Average_Order_Value
FROM dim_sales_territory st
JOIN
(
    SELECT
        SalesTerritoryKey,
        SalesOrderNumber,
        SalesAmount
    FROM fact_internet_sales

    UNION ALL

    SELECT
        SalesTerritoryKey,
        SalesOrderNumber,
        SalesAmount
    FROM fact_reseller_sales
) all_sales
    ON st.SalesTerritoryKey = all_sales.SalesTerritoryKey
GROUP BY
    st.SalesTerritoryRegion
ORDER BY Average_Order_Value DESC;


-- 8. INTERNET VS RESELLER SALES

SELECT
    'Internet' AS Sales_Channel,
    ROUND(SUM(SalesAmount), 2) AS Total_Sales
FROM fact_internet_sales

UNION ALL

SELECT
    'Reseller' AS Sales_Channel,
    ROUND(SUM(SalesAmount), 2) AS Total_Sales
FROM fact_reseller_sales;


-- 9. SALES BY PRODUCT CATEGORY

SELECT
    p.Category,
    ROUND(
        SUM(all_sales.SalesAmount),
        2
    ) AS Total_Sales
FROM dim_product p
JOIN
(
    SELECT
        ProductKey,
        SalesAmount
    FROM fact_internet_sales

    UNION ALL

    SELECT
        ProductKey,
        SalesAmount
    FROM fact_reseller_sales
) all_sales
    ON p.ProductKey = all_sales.ProductKey
GROUP BY p.Category
ORDER BY Total_Sales DESC;


-- 10. TOP 10 PRODUCTS BY SALES

SELECT
    p.Product,
    p.Category,
    p.Subcategory,
    ROUND(SUM(all_sales.SalesAmount), 2) AS Total_Sales
FROM dim_product p
JOIN
(
    SELECT
        ProductKey,
        SalesAmount
    FROM fact_internet_sales

    UNION ALL

    SELECT
        ProductKey,
        SalesAmount
    FROM fact_reseller_sales
) all_sales
    ON p.ProductKey = all_sales.ProductKey
GROUP BY
    p.ProductKey,
    p.Product,
    p.Category,
    p.Subcategory
ORDER BY Total_Sales DESC
LIMIT 10;


-- 11. SALES BY CUSTOMER OCCUPATION

SELECT
    c.Occupation,
    ROUND(SUM(f.SalesAmount), 2) AS Total_Sales,
    COUNT(DISTINCT c.CustomerKey) AS Number_of_Customers,
    ROUND(
        SUM(f.SalesAmount)
        / COUNT(DISTINCT c.CustomerKey),
        2
    ) AS Average_Sales_Per_Customer
FROM dim_customer c
JOIN fact_internet_sales f
    ON c.CustomerKey = f.CustomerKey
GROUP BY c.Occupation
ORDER BY Average_Sales_Per_Customer DESC;


-- 12. SALES BY YEARLY INCOME RANGE

SELECT
    CASE
        WHEN YearlyIncome < 30000 THEN 'Below 30K'
        WHEN YearlyIncome < 60000 THEN '30K-60K'
        WHEN YearlyIncome < 90000 THEN '60K-90K'
        WHEN YearlyIncome < 120000 THEN '90K-120K'
        ELSE '120K+'
    END AS Income_Group,

    COUNT(DISTINCT c.CustomerKey) AS Number_of_Customers,

    ROUND(SUM(f.SalesAmount), 2) AS Total_Sales,

    ROUND(
        SUM(f.SalesAmount)
        / COUNT(DISTINCT c.CustomerKey),
        2
    ) AS Average_Sales_Per_Customer

FROM dim_customer c
JOIN fact_internet_sales f
    ON c.CustomerKey = f.CustomerKey

GROUP BY
    CASE
        WHEN YearlyIncome < 30000 THEN 'Below 30K'
        WHEN YearlyIncome < 60000 THEN '30K-60K'
        WHEN YearlyIncome < 90000 THEN '60K-90K'
        WHEN YearlyIncome < 120000 THEN '90K-120K'
        ELSE '120K+'
    END

ORDER BY Average_Sales_Per_Customer DESC;


-- 13. SALES BY AGE GROUP

SELECT
    c.AgeGroup,
    COUNT(DISTINCT c.CustomerKey) AS Number_of_Customers,
    ROUND(SUM(f.SalesAmount), 2) AS Total_Sales,
    ROUND(
        SUM(f.SalesAmount)
        / COUNT(DISTINCT c.CustomerKey),
        2
    ) AS Average_Sales_Per_Customer
FROM dim_customer c
JOIN fact_internet_sales f
    ON c.CustomerKey = f.CustomerKey
GROUP BY c.AgeGroup
ORDER BY Average_Sales_Per_Customer DESC;


-- 14. TARGET AGE GROUPS UNDER 50

SELECT
    c.AgeGroup,
    COUNT(DISTINCT c.CustomerKey) AS Number_of_Customers,
    ROUND(SUM(f.SalesAmount), 2) AS Total_Sales,
    ROUND(
        SUM(f.SalesAmount)
        / COUNT(DISTINCT c.CustomerKey),
        2
    ) AS Average_Sales_Per_Customer
FROM dim_customer c
JOIN fact_internet_sales f
    ON c.CustomerKey = f.CustomerKey
WHERE c.AgeGroup IN
(
    '25-30',
    '30-35',
    '35-40',
    '40-45',
    '45-50'
)
GROUP BY c.AgeGroup
ORDER BY Average_Sales_Per_Customer DESC;


-- 15. CUSTOMER SEGMENTATION
-- OCCUPATION + INCOME

SELECT
    c.Occupation,

    CASE
        WHEN c.YearlyIncome < 30000 THEN 'Below 30K'
        WHEN c.YearlyIncome < 60000 THEN '30K-60K'
        WHEN c.YearlyIncome < 90000 THEN '60K-90K'
        WHEN c.YearlyIncome < 120000 THEN '90K-120K'
        ELSE '120K+'
    END AS Income_Group,

    COUNT(DISTINCT c.CustomerKey) AS Number_of_Customers,

    ROUND(SUM(f.SalesAmount), 2) AS Total_Sales,

    ROUND(
        SUM(f.SalesAmount)
        / COUNT(DISTINCT c.CustomerKey),
        2
    ) AS Average_Sales_Per_Customer

FROM dim_customer c
JOIN fact_internet_sales f
    ON c.CustomerKey = f.CustomerKey

GROUP BY
    c.Occupation,
    CASE
        WHEN c.YearlyIncome < 30000 THEN 'Below 30K'
        WHEN c.YearlyIncome < 60000 THEN '30K-60K'
        WHEN c.YearlyIncome < 90000 THEN '60K-90K'
        WHEN c.YearlyIncome < 120000 THEN '90K-120K'
        ELSE '120K+'
    END

ORDER BY Average_Sales_Per_Customer DESC;


-- 16. UNDERPERFORMING SALES TERRITORIES

SELECT
    st.SalesTerritoryRegion,

    ROUND(
        COALESCE(internet.InternetSales, 0)
        +
        COALESCE(reseller.ResellerSales, 0),
        2
    ) AS Total_Sales

FROM dim_sales_territory st

LEFT JOIN
(
    SELECT
        SalesTerritoryKey,
        SUM(SalesAmount) AS InternetSales
    FROM fact_internet_sales
    GROUP BY SalesTerritoryKey
) internet
    ON st.SalesTerritoryKey = internet.SalesTerritoryKey

LEFT JOIN
(
    SELECT
        SalesTerritoryKey,
        SUM(SalesAmount) AS ResellerSales
    FROM fact_reseller_sales
    GROUP BY SalesTerritoryKey
) reseller
    ON st.SalesTerritoryKey = reseller.SalesTerritoryKey

ORDER BY Total_Sales ASC;


-- 17. SALES BY COUNTRY

SELECT
    st.SalesTerritoryCountry,
    ROUND(
        SUM(COALESCE(internet.InternetSales, 0))
        + SUM(COALESCE(reseller.ResellerSales, 0)),
        2
    ) AS Total_Sales

FROM dim_sales_territory st

LEFT JOIN
(
    SELECT
        SalesTerritoryKey,
        SUM(SalesAmount) AS InternetSales
    FROM fact_internet_sales
    GROUP BY SalesTerritoryKey
) internet
    ON st.SalesTerritoryKey = internet.SalesTerritoryKey

LEFT JOIN
(
    SELECT
        SalesTerritoryKey,
        SUM(SalesAmount) AS ResellerSales
    FROM fact_reseller_sales
    GROUP BY SalesTerritoryKey
) reseller
    ON st.SalesTerritoryKey = reseller.SalesTerritoryKey

GROUP BY
    st.SalesTerritoryCountry

ORDER BY Total_Sales DESC;


-- 18. MONTHLY INTERNET SALES

SELECT
    YEAR(OrderDate) AS Sales_Year,
    MONTH(OrderDate) AS Sales_Month,
    ROUND(SUM(SalesAmount), 2) AS Total_Sales
FROM fact_internet_sales
GROUP BY
    YEAR(OrderDate),
    MONTH(OrderDate)
ORDER BY
    Sales_Year,
    Sales_Month;


-- 19. MONTHLY RESELLER SALES

SELECT
    YEAR(OrderDate) AS Sales_Year,
    MONTH(OrderDate) AS Sales_Month,
    ROUND(SUM(SalesAmount), 2) AS Total_Sales
FROM fact_reseller_sales
GROUP BY
    YEAR(OrderDate),
    MONTH(OrderDate)
ORDER BY
    Sales_Year,
    Sales_Month;


-- 20. TOP 10 CUSTOMERS BY SALES

SELECT
    c.CustomerKey,
    c.CustomerName,
    c.Occupation,
    c.YearlyIncome,
    ROUND(SUM(f.SalesAmount), 2) AS Total_Sales
FROM dim_customer c
JOIN fact_internet_sales f
    ON c.CustomerKey = f.CustomerKey
GROUP BY
    c.CustomerKey,
    c.CustomerName,
    c.Occupation,
    c.YearlyIncome
ORDER BY Total_Sales DESC
LIMIT 10;