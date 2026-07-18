import sqlite3
import pandas as pd

#Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

df_boston = pd.read_sql("""
                        SELECT e.firstName, e.lastName
                        FROM employees e
                        JOIN offices o ON e.officeCode = o.officeCode
                        WHERE o.city = 'Boston';
                        """, conn)

df_zero_emp = pd.read_sql("""
                          SELECT o.officeCode, o.city
                          FROM offices o
                          LEFT JOIN employees e ON o.officeCode = e.officeCode
                          WHERE e.employeeNumber IS NULL;
                          """, conn)



df_employee = pd.read_sql("""
                          SELECT e.firstName, e.lastName, o.city, o.state
                          FROM employees e
                          LEFT JOIN offices o ON e.officeCode = o.officeCode
                          ORDER BY e.firstName, e.lastName;
                          """, conn)



df_contacts = pd.read_sql("""
                          SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
                          FROM customers c
                          LEFT JOIN orders o ON c.customerNumber = o.customerNumber
                          WHERE o.orderNumber IS NULL
                          ORDER BY c.contactLastName;
                          """, conn)


df_payment = pd.read_sql("""
                         SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
                         FROM customers c
                         JOIN payments p ON c.customerNumber = p.customerNumber
                         ORDER BY CAST(p.amount AS REAL) DESC;
                         """, conn)


df_credit = pd.read_sql("""
                        SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
                        FROM employees e
                        JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                        GROUP BY e.employeeNumber
                        HAVING AVG(c.creditLimit) > 90000
                        ORDER BY num_customers DESC
                        LIMIT 4;
                        """, conn)

df_product_sold = pd.read_sql("""
                              SELECT p.productName,
                                     COUNT(o.orderNumber) AS numorders,
                                     SUM(od.quantityOrdered) AS totalunits
                              FROM products p
                              JOIN orderdetails od ON p.productCode = od.productCode 
                              JOIN orders o ON od.orderNumber = o.orderNumber
                              GROUP BY p.productName
                              ORDER BY totalunits DESC;
                              """, conn)

df_total_customers = pd.read_sql("""
                                 SELECT p.productName, p.productCode,
                                        COUNT(DISTINCT o.customerNumber) AS numpurchasers
                                 FROM products p
                                 JOIN orderdetails od ON p.productCode = od.productCode
                                 JOIN orders o ON od.orderNumber = o.orderNumber
                                 GROUP BY p.productName, p.productCode
                                 ORDER BY numpurchasers DESC;
                                 """, conn)


df_customers = pd.read_sql("""
                           SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
                           FROM offices o
                           JOIN employees e ON o.officeCode = e.officeCode
                           JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                           GROUP BY o.officeCode, o.city;
                           """, conn)


df_under_20 = pd.read_sql("""
                          WITH underperforming AS (
                              SELECT p.productCode
                              FROM products p
                              JOIN orderdetails od ON p.productCode = od.productCode
                              JOIN orders o ON od.orderNumber = o.orderNumber 
                              GROUP BY p.productCode
                              HAVING COUNT(DISTINCT o.customerNumber) < 20
                          )
                          SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
                          FROM employees e
                          JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                          JOIN orders ord ON c.customerNumber = ord.customerNumber
                          JOIN orderdetails od ON ord.orderNumber = od.orderNumber
                          JOIN underperforming u ON od.productCode = u.productCode
                          JOIN offices o ON e.officeCode = o.officeCode
                          GROUP BY e.employeeNumber
                          ORDER BY e.lastName;
                          """, conn)

results = {
    "Boston employees": df_boston,
    "Offices with zero employees": df_zero_emp,
    "Employees and offices": df_employee,
    "Customers without orders": df_contacts,
    "Payments": df_payment,
    "High-credit sales representatives": df_credit,
    "Products sold": df_product_sold,
    "Product purchasers": df_total_customers,
    "Customers per office": df_customers,
    "Employees who sold underperforming products": df_under_20,
}

if __name__ == "__main__":
    for title, dataframe in results.items():
        print(f"\n{title}\n{'-' * len(title)}")
        print(dataframe.to_string(index=False))

conn.close()