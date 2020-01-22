# coding: utf-8

"""
Creates a SQLite database from the data in the file buddymove_holidayiq.csv
(the BuddyMove dataset from UCI:
https://archive.ics.uci.edu/ml/datasets/BuddyMove+Data+Set), and then runs
queries on the database as per the Readme (LSDS 321 Assignment).
"""

import sqlite3
import pandas as pd

# Assigment - Part 2, Making and populating a Database:

# Load the data (use pandas) from the provided file buddymove_holidayiq.csv
# (the BuddyMove Data Set) - you should have 249 rows, 7 columns, and no
# missing values. The data reflects the number of place reviews by given
# users across a variety of categories (sports, parks, malls, etc.).
#
# Using the standard sqlite3 module:
# - Open a connection to a new (blank) database file
# buddymove_holidayiq.sqlite3
# - Use df.to_sql (documentation) to insert the data into a new table review
# in the SQLite3 database
#
# Then write the following queries (also with sqlite3) to test:
# - Count how many rows you have - it should be 249!
# - How many users who reviewed at least 100 Nature in the category also
# reviewed at least 100 in the Shopping category?
# - (Stretch) What are the average number of reviews for each category?


# Read in buddymove_holidayiq.csv file (the BuddyMove dataset from UCI) as a
# pandas dataframe:
buddymove_df = pd.read_csv('buddymove_holidayiq.csv')

# Check to make sure the 3 conditions in the prompt are satisfied:
# (1) 249 rows
# (2) 7 columns
# (3) no missing values
assert (buddymove_df.isnull().sum().sum() == 0) & (buddymove_df.shape[0] == 249) & (buddymove_df.shape[1] == 7)

print("\nLSDS 321 Assignment, Part 1: The data:")
print(buddymove_df)


# Open up a new connection + create new buddymove_holidayiq.sqlite3 DB:
conn = sqlite3.connect('buddymove_holidayiq.sqlite3')


# New cursor:
curs = conn.cursor()


# Add a table named 'review' with the buddymove_df data to our new
# buddymove_holidayiq.sqlite3 database
buddymove_df.to_sql('review', con=conn, if_exists='replace')


# Part 2 requirements and questions:
print("\nLSDS 321 Assignment, Part 2:")

# (1) 249 rows:
print("\n(1) Does the data table in the DB have 249 rows?:")
if curs.execute("SELECT COUNT('User Id') FROM review").fetchall()[0][0] == 249:
    print("Yes.")
else:
    print("No.")

# (2) "How many users who reviewed at least 100 Nature in the category
# also reviewed at least 100 in the Shopping category?":
print("""\n(2) How many users who reviewed at least 100 in the Nature category
also reviewed at least 100 in the Shopping category?:""")
num_users = curs.execute("SELECT COUNT('User Id') FROM review WHERE (Nature >= 100) AND (Shopping >= 100)").fetchall()[0][0]
print(f"{num_users} users")


# (3) "(Stretch) What are the average number of reviews for each category?"
print("\n(3) Stretch: What are the average number of reviews for each category?:")
avg_reviews_by_category = curs.execute("SELECT AVG(Sports), AVG(Religious), AVG(Nature), AVG(Theatre), AVG(Shopping), AVG(Picnic) FROM review").fetchall()
print(round(pd.DataFrame(avg_reviews_by_category, index=['avg_reviews'], columns=buddymove_df.columns.drop('User Id')), 1))


# Check answer to (3) above:
buddymove_df.mean()
