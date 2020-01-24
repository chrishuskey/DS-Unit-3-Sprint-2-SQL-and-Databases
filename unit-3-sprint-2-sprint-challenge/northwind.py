#!/usr/bin/env python
# coding: utf-8

# # LSDS Unit 3, Sprint 2 - SQL and Databases - Sprint Challenge (Chris Huskey)

# ### Part 2 - The Northwind Database
#
# Using `sqlite3`, connect to the given `northwind_small.sqlite3` database.
#
# ![Northwind Entity-Relationship Diagram](./northwind_erd.png)
#
# Above is an entity-relationship diagram - a picture summarizing the schema and
# relationships in the database. Note that it was generated using Microsoft
# Access, and some of the specific table/field names are different in the provided
# data. You can see all the tables available to SQLite as follows:
#
# ```python
# >>> curs.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY
# name;").fetchall()
# [('Category',), ('Customer',), ('CustomerCustomerDemo',),
# ('CustomerDemographic',), ('Employee',), ('EmployeeTerritory',), ('Order',),
# ('OrderDetail',), ('Product',), ('Region',), ('Shipper',), ('Supplier',),
# ('Territory',)]
# ```
#
# *Warning*: unlike the diagram, the tables in SQLite are singular and not plural
# (do not end in `s`). And you can see the schema (`CREATE TABLE` statement)
# behind any given table with:
# ```python
# >>> curs.execute('SELECT sql FROM sqlite_master WHERE name="Customer";').fetchall()
# [('CREATE TABLE "Customer" \n(\n  "Id" VARCHAR(8000) PRIMARY KEY, \n
# "CompanyName" VARCHAR(8000) NULL, \n  "ContactName" VARCHAR(8000) NULL, \n
# "ContactTitle" VARCHAR(8000) NULL, \n  "Address" VARCHAR(8000) NULL, \n  "City"
# VARCHAR(8000) NULL, \n  "Region" VARCHAR(8000) NULL, \n  "PostalCode"
# VARCHAR(8000) NULL, \n  "Country" VARCHAR(8000) NULL, \n  "Phone" VARCHAR(8000)
# NULL, \n  "Fax" VARCHAR(8000) NULL \n)',)]
# ```
#
# In particular note that the *primary* key is `Id`, and not `CustomerId`. On
# other tables (where it is a *foreign* key) it will be `CustomerId`. Also note -
# the `Order` table conflicts with the `ORDER` keyword! We'll just avoid that
# particular table, but it's a good lesson in the danger of keyword conflicts.
#
# Answer the following questions (each is from a single table):
#
# - What are the ten most expensive items (per unit price) in the database?
# - What is the average age of an employee at the time of their hiring? (Hint: a
#   lot of arithmetic works with dates.)
# - (*Stretch*) How does the average age of employee at hire vary by city?
#
# Your code (to load and query the data) should be saved in `northwind.py`, and
# added to the repository. Do your best to answer in purely SQL, but if necessary
# use Python/other logic to help.

import sqlite3


# Open up a new connection to our northwind_small.sqlite3 SQLite DB:
conn_northwind = sqlite3.connect('northwind_small.sqlite3')


# Open up a cursor for the connection:
curs = conn_northwind.cursor()


# List all the tables we have in our DB:
nw_list_of_tables = curs.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    ;
    """
).fetchall()

# Check to make sure they include all tables in the prompt:
assert nw_list_of_tables == [('Category',), ('Customer',), ('CustomerCustomerDemo',),
('CustomerDemographic',), ('Employee',), ('EmployeeTerritory',), ('Order',),
('OrderDetail',), ('Product',), ('Region',), ('Shipper',), ('Supplier',),
('Territory',)]

# Display names of all tables in our DB:
nw_list_of_tables


# Take a look at the original CREATE TABLE statement
# used to create the 'Customer' table in our DB:
curs.execute(
    """SELECT sql
    FROM sqlite_master
    WHERE name='Customer'
    ;
    """
).fetchall()

# CHECK: Should be (as per the prompt):
# [('CREATE TABLE "Customer" \n(\n  "Id" VARCHAR(8000) PRIMARY KEY, \n
# "CompanyName" VARCHAR(8000) NULL, \n  "ContactName" VARCHAR(8000) NULL, \n
# "ContactTitle" VARCHAR(8000) NULL, \n  "Address" VARCHAR(8000) NULL, \n  "City"
# VARCHAR(8000) NULL, \n  "Region" VARCHAR(8000) NULL, \n  "PostalCode"
# VARCHAR(8000) NULL, \n  "Country" VARCHAR(8000) NULL, \n  "Phone" VARCHAR(8000)
# NULL, \n  "Fax" VARCHAR(8000) NULL \n)',)]


# --------------------------------------------------

# Query #2.1: What are the ten most expensive items
# (per unit price) in the database?
print("\nQuery #2.1: What are the ten most expensive items in the database?")
most_expensive_products = curs.execute(
    """
    SELECT ProductName
    FROM Product, Supplier
    WHERE Product.SupplierId = Supplier.Id
    ORDER BY UnitPrice DESC
    LIMIT 10
    ;
    """
).fetchall()

# Include the product names in the list, by pulling the
# product names out of the tuples returned by fetchall() above:
for item_num in range(len(most_expensive_products)):
    most_expensive_products[item_num] = most_expensive_products[item_num][0]

# Print answer:
for product in most_expensive_products:
    print(product)


# --------------------------------------------------

# Query #2.2: What is the average age of an employee at the
# time of their hiring?
print("\nQuery #2.2: What is the avg. age of an employee at the time of hiring?")
avg_age_at_hiring = curs.execute(
    """
    SELECT AVG(AgeAtHiring)
    FROM (SELECT (HireDate - BirthDate) AS AgeAtHiring FROM Employee)
    ;
    """
).fetchone()[0]

# Print answer:
print(f"Employees' avg. age at hiring date: {round(avg_age_at_hiring, 0)}")


# --------------------------------------------------

# (Stretch)
# Query #2.3: How does the average age of employee at hire vary by city?


# ### Part 3 - Sailing the Northwind Seas
#
# You've answered some basic questions from the Northwind database, looking at
# individual tables - now it's time to put things together, and `JOIN`!
#
# Using `sqlite3` in `northwind.py`, answer the following:
#
# - What are the ten most expensive items (per unit price) in the database *and*
#   their suppliers?
# - What is the largest category (by number of unique products in it)?
# - (*Stretch*) Who's the employee with the most territories? Use `TerritoryId`
#   (not name, region, or other fields) as the unique identifier for territories.


# Query #3.1: What are the ten most expensive items
# (per unit price) in the database AND their suppliers?
print("\nQuery #3.1: What are the ten most expensive items in the database AND their suppliers?")
most_expensive_with_suppliers = curs.execute(
    """
    SELECT ProductName, Supplier.CompanyName
    FROM Product, Supplier
    WHERE Product.SupplierId = Supplier.Id
    ORDER BY UnitPrice DESC
    LIMIT 10
    ;
    """
).fetchall()

# Print answer:
product_num = 1
for product in most_expensive_with_suppliers:
    print(f"{product_num}. {product[0]} (Supplier: {product[1]})")
    product_num += 1


# --------------------------------------------------

# Query #3.2: What is the largest category (by # of unique products in it)?
print("\nQuery #3.2: What is the largest category (by number of unique products in it)?")
largest_category = curs.execute(
    """
    SELECT CategoryName, MAX(num_products)
    FROM
    (SELECT COUNT(DISTINCT Product.Id) AS num_products, Category.CategoryName
    FROM Product, Category
    WHERE Product.CategoryId = Category.Id
    GROUP BY CategoryId
    ORDER BY num_products DESC)
    ;
    """
).fetchone()

# Print answer:
print(f"Largest category: {largest_category[0]} ({largest_category[1]} unique products)")


# --------------------------------------------------

# (Stretch)
# Query #3.3: Who's the employee with the most territories?
# Use TerritoryId (not name, region, or other fields) as the
# unique identifier for territories.


# Close our cursor, commit the connection,
# close the connection:
conn_northwind.commit()
curs.close()
conn_northwind.close()
