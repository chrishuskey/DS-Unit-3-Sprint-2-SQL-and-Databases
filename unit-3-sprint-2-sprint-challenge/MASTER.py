#!/usr/bin/env python
# coding: utf-8

# # LSDS Unit 3, Sprint 2 - SQL and Databases - Sprint Challenge (Chris Huskey)

# ### Part 1 - Making and populating a Database:
# 
# Consider the following data:
# 
# | s   | x | y |
# |-----|---|---|
# | 'g' | 3 | 9 |
# | 'v' | 5 | 7 |
# | 'f' | 8 | 7 |
# 
# Using the standard `sqlite3` module:
# 
# - Open a connection to a new (blank) database file `demo_data.sqlite3`
# - Make a cursor, and execute an appropriate `CREATE TABLE` statement to accept
#   the above data (name the table `demo`)
# - Write and execute appropriate `INSERT INTO` statements to add the data (as
#   shown above) to the database
# 
# Make sure to `commit()` so your data is saved! The file size should be non-zero.
# 
# Then write the following queries (also with `sqlite3`) to test:
# 
# - Count how many rows you have - it should be 3!
# - How many rows are there where both `x` and `y` are at least 5?
# - How many unique values of `y` are there (hint - `COUNT()` can accept a keyword
#   `DISTINCT`)?
# 
# Your code (to reproduce all above steps) should be saved in `demo_data.py` and
# added to the repository along with the generated SQLite database.

# In[1]:


import sqlite3


# In[2]:


# Open up a new connection to our SQLite DB:
conn_demodb = sqlite3.connect('demo_data.sqlite3')


# In[3]:


# Open up a cursor for the connection:
curs = conn_demodb.cursor()


# In[5]:


# Create new table name demo in our SQLite DB demo_data.sqlite3 
# for the Part 1 demo data:
curs.execute(
    """
    CREATE TABLE demo (
        s  VARCHAR(50)  NOT NULL, 
        x  INT          NOT NULL, 
        y  INT          NOT NULL
    );
    """
)

# And commit the connection to our DB:
conn_demodb.commit()


# In[6]:


# Insert the Part 1 demo data into our demo table:
curs.execute(
    """
    INSERT INTO demo(s, x, y) 
    VALUES 
    ('g', 3, 9), 
    ('v', 5, 7), 
    ('f', 8, 7)
    ;
    """
)


# In[11]:


# Check to make sure our DB includes the data inserted above:
curs.execute(
    """
    SELECT * FROM demo;
    """
).fetchall()


# In[52]:


# Query #1: How many rows does our demo table have?
print("Query #1: How many rows does our demo table have?")

# Should be 3 rows:
assert demo_num_rows == 3

# Print result:
demo_num_rows = curs.execute(
    """
    SELECT COUNT(*) 
    FROM demo
    ;
    """
).fetchone()[0]
print(f"{demo_num_rows} rows")

# -------------------------------------------------------

# Query #2: How many rows are there where 
# both x and y are at least 5?
print("""\nQuery #2: How many rows where both x and y are at least 5?""")

# Print answer:
query02_rows = curs.execute(
    """
    SELECT COUNT(*) 
    FROM demo 
    WHERE (x >= 5) AND (y >= 5)
    ;
    """
).fetchall()[0][0]
print(f"{query02_rows} rows")

# -------------------------------------------------------

# Query #3: How many unique values of y are there 
# (hint - COUNT() can accept a keyword DISTINCT)?
print("\nQuery #3: How many unique values of y are there?")

# Print result:
query03_rows = curs.execute(
    """
    SELECT COUNT(DISTINCT y) 
    FROM demo
    ;
    """
).fetchone()[0]
print(f"{query03_rows} unique values of y")


# In[57]:


# Close our cursor, commit the connection, 
# close the connection:
curs.close()
conn_demodb.commit()
conn_demodb.close()


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

# In[58]:


import sqlite3


# In[59]:


# Open up a new connection to our northwind_small.sqlite3 SQLite DB:
conn_northwind = sqlite3.connect('northwind_small.sqlite3')


# In[60]:


# Open up a cursor for the connection:
curs = conn_northwind.cursor()


# In[67]:


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


# In[69]:


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


# In[111]:


# Query #1: What are the ten most expensive items 
# (per unit price) in the database?
print("Query #1: What are the ten most expensive items in the database?")
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

# -------------------------------------------------------

# Query #2: What is the average age of an employee at the 
# time of their hiring?
print("\nQuery #2: What is the avg. age of an employee at the time of hiring?")
avg_age_at_hiring = curs.execute(
    """
    SELECT AVG(AgeAtHiring) 
    FROM (SELECT (HireDate - BirthDate) AS AgeAtHiring FROM Employee)
    ;
    """
).fetchone()[0]

# Print answer:
print(f"Employees' avg. age at hiring date: {round(avg_age_at_hiring, 0)}")

# -------------------------------------------------------

# (Stretch) 
# Query #3: How does the average age of employee at hire vary by city?


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

# In[134]:


# Query #1: What are the ten most expensive items 
# (per unit price) in the database AND their suppliers?
print("Query #1: What are the ten most expensive items in the database AND their suppliers?")
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

# -------------------------------------------------------

# Query #2: What is the largest category (by # of unique products in it)?
print("\nQuery #2: What is the largest category (by number of unique products in it)?")
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

# -------------------------------------------------------

# (Stretch)
# Query #3: Who's the employee with the most territories? 
# Use TerritoryId (not name, region, or other fields) as the 
# unique identifier for territories.


# In[135]:


# Close our cursor, commit the connection, 
# close the connection:
conn_northwind.commit()
curs.close()
conn_northwind.close()


# ### Part 4 - Questions (and your Answers)
# 
# Answer the following questions, baseline ~3-5 sentences each, as if they were
# interview screening questions (a form you fill when applying for a job):
# 
# - In the Northwind database, what is the type of relationship between the
#   `Employee` and `Territory` tables?
# - What is a situation where a document store (like MongoDB) is appropriate, and
#   what is a situation where it is not appropriate?
# - What is "NewSQL", and what is it trying to achieve?

# In[ ]:


# See markdown file.


# In[ ]:


# Question #1: In the Northwind database, what is the type of 
# relationship between the `Employee` and `Territory` tables?

# Answer:
# The Territory table is connected to the Employee Territory 
# table via TerritoryId (key Id in the Territory table = TerritoryId 
# in the EmployeeTerritory table), and the EmployeeTerritory 
# table is connected to the Employee table via the EmployeeId key 
# (key Id in the Employee table = EmployeeId in the EmployeeTerritory 
# table).
# 
# So you could do an implicit join via a WHERE statement in 
# query as below:
# WHERE (Employee.Id = EmployeeTerritory.EmployeeId) AND 
# (EmployeeTerritory.TerritoryId = Territory.Id)

# -------------------------------------------------------

# Question #2: What is a situation where a document store 
# (like MongoDB) is appropriate, and what is a situation where it is not appropriate?

# Answer:
# A document store DB like MongoDB that stores JSON docs 
# (JSON docs are data formatted as key:value pairs) can be very 
# useful when you have truly massive amounts of data, such that 
# storing the entire DB in one single place (e.g., one 
# HW device/server) to use it as a relational database would 
# be far too expensive or even impossible (require vertical 
# scaling your HW to a point at which it is extremely 
# expensive, or maybe does not even exist yet). In such a 
# situation, a document store DB ("NoSQL DB" / non-relational 
# DB) can be extremely useful and more much cost-efficient, 
# because it can allow you to distribute the compute task/process 
# across many cheaper (and existing today) HW devices, using 
# much more cost-efficient parallel processing / distributed 
# computing approach. For example (one method -- MapReduce): 
# sharding your data into many different parts
# --> run a map operation to sort or filter each shard of 
# local data as needed 
# --> run a reduce operation to process and operation on each 
# local shard of data and combine all into the final result we want.
# (a MapReduce approach, as used in Hadoop HDFS-es)
# 
# A document store DB would not be as appropriate for a situation 
# in which having well-structured, quickly queryable data is your 
# #1 priority. For example, if your database is meant primarily 
# for your business analysts to query using SQL, and you don't 
# have truly massive amounts of data (e.g., 10,000s of customers, 
# products, orders instead of 10 mns of customers, products, 
# orders).

# -------------------------------------------------------

# Question #3: What is "NewSQL", and what is it trying to achieve?

# Answer:
# NewSQL DB solutions aim to combine the ease-of-use of SQL in the form 
# of queries via SQL (Structured Query Language) with the horizontal 
# scalability and connected greater computational cost-efficiency 
# possible with non-relational (document store or "NoSQL") DBs.


# ### Part 5 - Turn it in!
# Provide all the files you wrote (`demo_data.py`, `northwind.py`), as well as
# this file with your answers to part 4, directly to your TL. You're also
# encouraged to include the output from your queries as docstring comments, to
# facilitate grading and feedback. Thanks for your hard work!
# 
# If you got this far, check out the [larger Northwind
# database](https://github.com/jpwhite3/northwind-SQLite3/blob/master/Northwind_large.sqlite.zip) -
# your queries should run on it as well, with richer results.

# In[ ]:


# See .py files in this directory/repo.

