## Introduction

In this lab, you'll practice your knowledge of JOIN statements and subqueries, using various types of joins and various methods for specifying the links between them. One of the main benefits of using a relational database is table relations, which allow you to access and connect data via shared columns. By writing more advanced SQL queries that utilize joins and subqueries, you can provide a deeper and more granular level of analysis and data retrieval.

This assessment continues looking at the familiar Northwind/CRM database (`data.sqlite`) that contains customer relationship management data as well as employee and product data. Your code for this lab is in `main.py`. You can run `pytest` and use print statements to check your code as you go.

## Learning Objectives

* Write SQL queries that make use of various types of joins.
* Perform the best type of join for retrieving the desired data.
* Write subqueries to decompose complex queries.
* Limit the number of records returned by a query using `LIMIT`.
* Use `GROUP BY` statements in SQL to apply aggregate functions.

## Set Up

Run `pipenv install` and `pipenv shell`. You can run the test suite at any time with `pytest`, or check print statement outputs with `python3 main.py`.

## Part 1: Join and Filter

* Return the first and last names and job titles for all employees in Boston (`df_boston_employees`).
* Are there any offices that have zero employees (`df_ghost_offices`)?

## Part 2: Type of Join

* Return all employees' first and last names along with the city/state of the office they work out of, if any. Include all employees, ordered by first name then last name (`df_all_employees_offices`).
* Return contact info (first name, last name, phone) and sales rep employee number for customers who have not placed an order, sorted alphabetically by last name (`df_customers_no_orders`). 24 customers have not placed an order.

## Part 3: Built-In Function

* Return customer contacts' first/last names along with each payment's amount and date, sorted descending by amount (`df_customer_payments`). Note: `amount` is stored as text, so it must be `CAST` to a numeric type before sorting.

## Part 4: Joining and Grouping

* Return employee number, first name, last name, and number of customers (`numCustomers`) for employees whose customers have an average credit limit over 90k, sorted by number of customers descending (`df_high_credit_reps`). There are 4 such employees.
* Return product name, count of orders (`numorders`), and total quantity sold (`totalunits`) per product, sorted by `totalunits` descending (`df_top_products`).

## Part 5: Multiple Joins

* Return product name, product code, and count of distinct customers who ordered each product (`numpurchasers`), sorted descending (`df_product_purchasers`).
* Return office code, city, and count of customers per office (`n_customers`) (`df_office_customers`).

## Part 6: Subquery

* Using a subquery, return employee number, first name, last name, office city, and office code for employees who sold products ordered by fewer than 20 distinct customers (`df_underperforming_product_employees`).

## Close the connection

```python
conn.close()
```
