# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("data.sqlite")

print(pd.read_sql("""SELECT * FROM sqlite_master""", conn))


# ------------------------------------------------------------------
# Part 1: Join and Filter
# ------------------------------------------------------------------

# Boston employees: first name, last name, job title
df_boston_employees = pd.read_sql("""
SELECT firstName, lastName, jobTitle
FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
WHERE offices.city = "Boston"
""", conn)
print("---------------------Boston Employees---------------------")
print(df_boston_employees)
print("-------------------End Boston Employees-------------------")

# Offices with zero employees ("ghost" locations)
df_ghost_offices = pd.read_sql("""
SELECT offices.officeCode, offices.city, COUNT(employees.employeeNumber) AS numEmployees
FROM offices
LEFT JOIN employees ON offices.officeCode = employees.officeCode
GROUP BY offices.officeCode
HAVING COUNT(employees.employeeNumber) = 0
""", conn)
print("---------------------Ghost Offices---------------------")
print(df_ghost_offices)
print("-------------------End Ghost Offices-------------------")


# ------------------------------------------------------------------
# Part 2: Type of Join
# ------------------------------------------------------------------

# All employees with their office's city/state (if any), ordered by name
df_all_employees_offices = pd.read_sql("""
SELECT employees.firstName, employees.lastName, offices.city, offices.state
FROM employees
LEFT JOIN offices ON employees.officeCode = offices.officeCode
ORDER BY employees.firstName, employees.lastName
""", conn)
print("---------------------Employees & Offices---------------------")
print(df_all_employees_offices)
print("-------------------End Employees & Offices-------------------")

# Customers who have not placed any orders
df_customers_no_orders = pd.read_sql("""
SELECT customers.contactFirstName, customers.contactLastName, customers.phone, customers.salesRepEmployeeNumber
FROM customers
LEFT JOIN orders ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY customers.contactLastName
""", conn)
print("---------------------Customers With No Orders---------------------")
print(df_customers_no_orders)
print("-------------------End Customers With No Orders-------------------")


# ------------------------------------------------------------------
# Part 3: Built-In Function
# ------------------------------------------------------------------

# Customer payments, sorted by amount (cast to numeric since it's stored as text)
df_customer_payments = pd.read_sql("""
SELECT customers.contactFirstName, customers.contactLastName, payments.amount, payments.paymentDate
FROM customers
JOIN payments ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC
""", conn)
print("---------------------Customer Payments---------------------")
print(df_customer_payments)
print("-------------------End Customer Payments-------------------")


# ------------------------------------------------------------------
# Part 4: Joining and Grouping
# ------------------------------------------------------------------

# Employees whose customers have an average credit limit over 90k
df_high_credit_reps = pd.read_sql("""
SELECT employees.employeeNumber, employees.firstName, employees.lastName, COUNT(customers.customerNumber) AS numCustomers
FROM employees
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employees.employeeNumber
HAVING AVG(customers.creditLimit) > 90000
ORDER BY numCustomers DESC
""", conn)
print("---------------------High Credit Sales Reps---------------------")
print(df_high_credit_reps)
print("-------------------End High Credit Sales Reps-------------------")

# Top-selling products by total units ordered
df_top_products = pd.read_sql("""
SELECT products.productName, COUNT(orderdetails.orderNumber) AS numorders, SUM(orderdetails.quantityOrdered) AS totalunits
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
GROUP BY products.productCode
ORDER BY totalunits DESC
""", conn)
print("---------------------Top Products---------------------")
print(df_top_products)
print("-------------------End Top Products-------------------")


# ------------------------------------------------------------------
# Part 5: Multiple Joins
# ------------------------------------------------------------------

# Number of distinct customers who ordered each product
df_product_purchasers = pd.read_sql("""
SELECT products.productName, products.productCode, COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products
JOIN orderdetails ON products.productCode = orderdetails.productCode
JOIN orders ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode
ORDER BY numpurchasers DESC
""", conn)
print("---------------------Product Purchasers---------------------")
print(df_product_purchasers)
print("-------------------End Product Purchasers-------------------")

# Number of customers per office
df_office_customers = pd.read_sql("""
SELECT offices.officeCode, offices.city, COUNT(customers.customerNumber) AS n_customers
FROM offices
LEFT JOIN employees ON offices.officeCode = employees.officeCode
LEFT JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode
""", conn)
print("---------------------Customers Per Office---------------------")
print(df_office_customers)
print("-------------------End Customers Per Office-------------------")


# ------------------------------------------------------------------
# Part 6: Subquery
# ------------------------------------------------------------------

# Employees who sold products ordered by fewer than 20 distinct customers
df_underperforming_product_employees = pd.read_sql("""
SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.officeCode
FROM employees
JOIN offices ON employees.officeCode = offices.officeCode
JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders ON customers.customerNumber = orders.customerNumber
JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
WHERE orderdetails.productCode IN (
    SELECT orderdetails.productCode
    FROM orderdetails
    JOIN orders ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY orderdetails.productCode
    HAVING COUNT(DISTINCT orders.customerNumber) < 20
)
""", conn)
print("---------------------Underperforming Product Sellers---------------------")
print(df_underperforming_product_employees)
print("-------------------End Underperforming Product Sellers-------------------")


conn.close()
