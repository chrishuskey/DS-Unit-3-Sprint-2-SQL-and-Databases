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


# Open up a new connection to our SQLite DB:
conn_demodb = sqlite3.connect('demo_data.sqlite3')


# Open up a cursor for the connection:
curs = conn_demodb.cursor()


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


# Check to make sure our DB includes the data inserted above:
curs.execute(
    """
    SELECT * FROM demo;
    """
).fetchall()


# Query #1: How many rows does our demo table have?
print("Query #1: How many rows does our demo table have?")

# Print result:
demo_num_rows = curs.execute(
    """
    SELECT COUNT(*)
    FROM demo
    ;
    """
).fetchone()[0]
print(f"{demo_num_rows} rows")

# Should be 3 rows:
assert demo_num_rows == 3


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


# Close our cursor, commit the connection,
# close the connection:
curs.close()
conn_demodb.commit()
conn_demodb.close()
