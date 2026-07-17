import sqlite3
import pandas as pd
from main import *

def test_connection():
    assert(type(conn) == sqlite3.Connection)

def test_step2():
    assert(df_first_five.shape == (23, 2))
    assert(list(df_first_five.columns) == ['employeeNumber', 'lastName'])

def test_step_3():
    assert(df_five_reverse.shape == (23, 2))
    assert(list(df_five_reverse.columns) == ['lastName', 'employeeNumber'])

def test_step4():
    assert('ID' in df_alias.columns)

def test_step5():
    assert('role' in df_executive.columns)
    for x in ['Executive', 'Not Executive']:
        for x in list(df_executive['role']):
            assert(x)

def test_step6():
    assert('name_length' in df_name_length.columns)
    assert(df_name_length.iloc[0]['name_length'] == 6)
        
def test_step7():
    assert('short_title' in df_short_title.columns)
    assert(df_short_title.iloc[0]['short_title'] == 'Pr')

def test_step8():
    assert(sum_total_price[0] == 9604251)

def test_step9():
    for x in ['day', 'month', 'year']:
        for x in df_day_month_year.columns:
            assert(x)
    assert(df_day_month_year.iloc[0]['day'] == '06')