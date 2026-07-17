import sqlite3
from main import *


def test_connection():
    assert(type(conn) == sqlite3.Connection)


# Part 1: Join and Filter

def test_boston_employees():
    assert(list(df_boston_employees.columns) == ['firstName', 'lastName', 'jobTitle'])
    assert(df_boston_employees.shape[0] == 2)
    assert(set(df_boston_employees['lastName']) == {'Firrelli', 'Patterson'})


def test_ghost_offices():
    assert(list(df_ghost_offices.columns) == ['officeCode', 'city', 'numEmployees'])
    assert((df_ghost_offices['numEmployees'] == 0).all())


# Part 2: Type of Join

def test_all_employees_offices():
    assert(list(df_all_employees_offices.columns) == ['firstName', 'lastName', 'city', 'state'])
    assert(df_all_employees_offices.shape[0] == 23)
    firsts = list(df_all_employees_offices['firstName'])
    assert(firsts == sorted(firsts))


def test_customers_no_orders():
    assert(list(df_customers_no_orders.columns) == ['contactFirstName', 'contactLastName', 'phone', 'salesRepEmployeeNumber'])
    assert(df_customers_no_orders.shape[0] == 24)
    last_names = list(df_customers_no_orders['contactLastName'])
    assert(last_names == sorted(last_names))


# Part 3: Built-In Function

def test_customer_payments():
    assert('amount' in df_customer_payments.columns and 'paymentDate' in df_customer_payments.columns)
    amounts = df_customer_payments['amount'].astype(float)
    assert(list(amounts) == sorted(amounts, reverse=True))


# Part 4: Joining and Grouping

def test_high_credit_reps():
    assert(list(df_high_credit_reps.columns) == ['employeeNumber', 'firstName', 'lastName', 'numCustomers'])
    assert(df_high_credit_reps.shape[0] == 4)
    counts = list(df_high_credit_reps['numCustomers'])
    assert(counts == sorted(counts, reverse=True))


def test_top_products():
    assert('numorders' in df_top_products.columns and 'totalunits' in df_top_products.columns)
    totals = list(df_top_products['totalunits'])
    assert(totals == sorted(totals, reverse=True))


# Part 5: Multiple Joins

def test_product_purchasers():
    assert('numpurchasers' in df_product_purchasers.columns)
    assert('productCode' in df_product_purchasers.columns)
    purchasers = list(df_product_purchasers['numpurchasers'])
    assert(purchasers == sorted(purchasers, reverse=True))


def test_office_customers():
    assert(list(df_office_customers.columns) == ['officeCode', 'city', 'n_customers'])
    assert(df_office_customers.shape[0] == 7)


# Part 6: Subquery

def test_underperforming_product_employees():
    assert(list(df_underperforming_product_employees.columns) == ['employeeNumber', 'firstName', 'lastName', 'city', 'officeCode'])
    assert(df_underperforming_product_employees.shape[0] > 0)
    assert(df_underperforming_product_employees['employeeNumber'].duplicated().sum() == 0)
